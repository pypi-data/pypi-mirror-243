import itertools
import platform
import sys
from enum import Enum
from getpass import getuser
from typing import Any, Generic, TypeVar

import httpx
from pydantic import BaseModel

from .stepper import Stepper, StepResult, StepStatus

try:
    from tqdm.auto import tqdm
except ImportError:
    tqdm = None

try:
    import polars as pl
except ImportError:
    pl = None

try:
    import pandas as pd
except ImportError:
    pd = None


class RunnerError(Exception):
    pass


class RunnerSetupError(RunnerError):
    pass


class ProjectNotFoundError(RunnerError):
    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message

    def __str__(self) -> str:
        return self.message


class TestRunModel(BaseModel):
    id: int | None = None
    project_id: int
    short_code: str
    dut_id: str
    machine_hostname: str
    user_name: str
    test_name: str
    data: dict | None = None


T = TypeVar("T")
U = TypeVar("U")


class StatefulResult(Generic[T, U]):
    def __init__(self, result: T, state: U) -> None:
        self._result = result
        self._state = state

    @property
    def result(self) -> T:
        return self._result

    @property
    def state(self) -> U:
        return self._state


class MeasurementRunState(Enum):
    NEW = 1
    EXISTING = 2
    IN_PROGRESS = 3
    FAILED = 4
    DONE = 5


class MeasurementRun:
    def __init__(
        self,
        testrun_id: int,
        client: httpx.AsyncClient,
        steps: list[Any],
        steppers: dict[str, Stepper],
    ):
        self.client = client
        self.steps = steps
        self.sequence_number = 0
        self.steppers = steppers
        self.testrun_id = testrun_id

    async def set_state(self, state: str):
        if state == "running":
            action = "start"
        elif state == "failed":
            action = "fail"
        elif state == "complete":
            action = "complete"

        r = await self.client.put(f"/api/testruns/{action}/{self.testrun_id}")
        # TODO: make error information a bit prettier
        if r.status_code != 200:
            raise RunnerError(r.json())

    async def step(self):
        if self.sequence_number > len(self.steps):
            raise IndexError("already went through all the steps")

        current_step = self.steps[self.sequence_number]

        step_results: dict[str, str | float] = {}

        for k, v in current_step.items():
            if k == "idx":
                continue

            # technically items within a step should be independent so
            # we could also execute them in parallel here
            res: StepResult | None = self.steppers[k].step(v)

            if res is None:
                continue

            if res.status == StepStatus.success:
                if res.value is not None:
                    step_results[k] = res.value
            elif res.status == StepStatus.failed:
                await self.set_state("failed")
                raise RunnerError(f"step {self.sequence_number}, {k}:{v} failed")

        r = await self.client.post(
            "/api/measurement_entries/batch",
            json={
                "sequence_number": self.sequence_number,
                "testrun_id": self.testrun_id,
                "payload": step_results,
            },
        )

        # TODO: proper error handling
        if r.status_code != 201:
            raise RunnerError(r.json())

        self.sequence_number += 1

    @property
    def _parquet_url(self) -> str:
        return f"/api/testruns/measurements/{self.testrun_id}?format=parquet"

    async def polars_df(self) -> "pl.DataFrame":
        if pl:
            r = await self.client.get(self._parquet_url)
            return pl.read_parquet(r.content)
        raise NotImplementedError("optional polars dependency is unavailable")

    async def pandas_df(self) -> "pd.DataFrame":
        if pd:
            r = await self.client.get(self._parquet_url)
            return pd.read_parquet(r.content)
        raise NotImplementedError("optional pandas dependency is unavailable")


class MeasurementRunner:
    project_id: int | None = None
    current_step: int | None = None
    testrun_id: int | None = None
    extra_run_data: dict[str, Any] | None = None

    def __init__(
        self,
        ms_url: str,
        project_number: str,
        extra_run_data: dict[str, Any] | None = None,
        client: httpx.AsyncClient | None = None,
        client_headers: dict[str, str] | None = None,
    ) -> None:
        self.ms_url = ms_url.rstrip("/")
        self.project_number = project_number
        self.extra_run_data = extra_run_data

        self.client = (
            httpx.AsyncClient(base_url=self.ms_url, headers=client_headers)
            if client is None
            else client
        )

    async def run(
        self,
        steps: list[dict],
        steppers: dict[str, Stepper],
        short_code: str,
        dut_id: str,
        test_name: str,
    ) -> MeasurementRun:
        """run executes the test plan or returns the already existing plan if called
        with the same short_code again.
        """

        # 1. check if the project exists and get the project id
        setup_res = await self.setup_run(steps, steppers, short_code, dut_id, test_name)
        run = setup_res.result

        if setup_res.state != MeasurementRunState.NEW:
            return run

        # 2. set our testrun to the running state
        await run.set_state("running")

        # display a progress bar when running interactively
        if hasattr(sys, "ps1") and tqdm:
            steps = tqdm(steps, desc=f"SC: {short_code}, DUT: {dut_id}", unit="step")

        # 3. run the steps
        for _ in steps:
            await run.step()

        # 4. set the run as completed
        await run.set_state("complete")

        return run

    async def setup_run(
        self,
        steps: list[dict],
        steppers: dict[str, Stepper],
        short_code: str,
        dut_id: str,
        test_name: str,
    ) -> StatefulResult[MeasurementRun, MeasurementRunState]:
        await self._init_project()

        tr = await self._ensure_testrun(short_code, dut_id, test_name)

        # create a MeasurementRun helper class from the testrun
        mr = MeasurementRun(tr.result.id, self.client, steps, steppers)

        # don't continue with the setup if the run already exists
        if tr.state == MeasurementRunState.EXISTING:
            return StatefulResult(mr, tr.state)

        # 2.1. get information form the steppers
        columns: dict[str, dict] = {
            name: {
                "data_source": s.data_source(),
                "description": s.description(),
                "measurement_unit": s.measurement_unit(),
            }
            for name, s in steppers.items()
        }

        # 2.2. create all the setup data
        r = await self.client.post(
            f"/api/testruns/setup/{tr.result.id}",
            json={
                "steps": steps,
                "columns": columns,
            },
        )
        if r.status_code != 200:
            raise RunnerError(
                f"could not set up run, status: {r.status_code}, response: {r.text}"
            )

        return StatefulResult(mr, tr.state)

    async def _ensure_testrun(
        self, short_code: str, dut_id: str, test_name: str
    ) -> StatefulResult[TestRunModel, MeasurementRunState]:
        """_ensure_testrun checks if this testrun already exists and returns it
        instead of creating a duplicate.

        returns a StatefulResult with the model and the status of the run.
        """
        testrun_id: int | None = None
        mod: TestRunModel | None = None

        # check if this testrun already exists
        r = await self.client.get(f"/api/testruns/{short_code}")
        if r.status_code == 200:
            mod = TestRunModel.parse_obj(r.json())
            testrun_id = mod.id

        run = TestRunModel(
            id=testrun_id,
            project_id=self.project_id,
            short_code=short_code,
            dut_id=dut_id,
            machine_hostname=platform.node(),
            user_name=getuser(),
            test_name=test_name,
            data=self.extra_run_data,
        )

        # check if parameters changed and err out or return the existing run
        if mod:
            if run == mod:
                return StatefulResult(mod, MeasurementRunState.EXISTING)

            msg = (
                "testrun with this short code but different params already exists\n"
                f"remote: {mod}\n"
                f"local: {run}"
            )
            raise RunnerSetupError(msg)

        # create a new testrun if it doesn't exist yet
        r = await self.client.post("/api/testruns", json=run.model_dump())
        if r.status_code != 201:
            raise RunnerSetupError(r.json())

        run.id = r.json()["id"]

        return StatefulResult(run, MeasurementRunState.NEW)

    async def _init_project(self):
        # check if the project id is set and fetch it from the ms otherwise
        if self.project_id is None:
            r = await self.client.get(f"/api/projects/{self.project_number}")
            if r.status_code == 404:
                raise ProjectNotFoundError(
                    f"project {self.project_number} not found in edea-ms"
                )
            self.project_id = r.json()["id"]


def condition_generator(
    test_parameters: dict[list[float | str]],
) -> list[dict[str, str | float]]:
    """
    General-purpose test condition generator.
    Takes a map of Stepper names as key with the conditions as a list of values. It will
    generate a list of set-conditions in order of the keys and values.

    It generates a set of conditions for each key. The values of each key are iterated
    in order and the keys from last to first.
    The key order should represent significance of change, e.g. how long it takes for a
    condition to be reached.

    To visualize this, an input of {"a": [1, 2], "b": ["foo", "bar"], "c": [3, 4]} will
    result in the following output:
    [
        {"a": 1, "b": "foo", "c": 3},
        {"a": 1, "b": "foo", "c": 4},
        {"a": 1, "b": "bar", "c": 3},
        {"a": 1, "b": "bar", "c": 4},
        {"a": 2, "b": "foo", "c": 3},
        {"a": 2, "b": "foo", "c": 4},
        {"a": 2, "b": "bar", "c": 3},
        {"a": 2, "b": "bar", "c": 4},
    ]
    """

    test_conditions = []
    for idx, e in enumerate(itertools.product(*test_parameters.values())):
        d = {"idx": idx}
        for subindex, key in enumerate(test_parameters.keys()):
            d[key] = e[subindex]
        test_conditions.append(d)
    return test_conditions
