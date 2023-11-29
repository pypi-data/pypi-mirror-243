from enum import Enum

from pydantic import BaseModel


class StepStatus(str, Enum):
    """
    TODO add state diagram here
    """

    done = "done"
    success = "success"
    failed = "failed"
    scheduled = "scheduled"
    ignored = "ignored"

class Step(BaseModel):
    index: int
    to_set: dict[str, float | str] # don't expect a result
    to_measure: dict[str, float | str] # expect a result

class StepResult:
    status: StepStatus
    value: str | float | None

    def __init__(
        self, status: StepStatus = StepStatus.success, value: str | float | None = None
    ) -> None:
        self.status = status
        self.value = value


class Stepper:
    _depends_on: list[str]

    def __init__(self, depends_on: list[str]) -> None:
        self._depends_on = depends_on

    def setup(self, resume: bool = False):
        """
        setup the device/instrument/other based on the parameters passed
        in the class initialization. resume will
        """
        pass

    def pre_step(self):
        """
        pre_step will be executed before a new step is being run. this can
        e.g. be a sanity check that a value is in an expected range for the
        next step to be run.
        """
        pass

    def step(self, set_point: str | float) -> StepResult:
        """
        step brings the device/instrument/other to a given setpoint and returns
        a result representing success or failure. on success, post_step will be
        executed and on failure, depending on the result of the check method,
        it will be re-tried (check says it's ok) or the procedure will be aborted.
        """
        pass

    def post_step(self):
        """
        post_step, similar to pre_step is an additional check that will be
        executed after a step has been executed for a given set point.
        """
        pass

    def teardown(self):
        """
        teardown will be run after a run has been finished. this should bring
        everything that needs it into a safe state and/or shut it off if
        necessary.
        """
        pass

    def depends_on(self, step: str) -> bool:
        """
        depends_on returns true if the given step should be executed before it
        """
        return step in self._depends_on

    def data_source(self) -> str | None:
        """
        data_source should return what kind of data source this is, e.g. DMMch1
        """
        return None

    def description(self) -> str | None:
        """
        description property which specifies in human-readable form what this Stepper is
        e.g. "DMM Channel 1"
        """
        return None

    def measurement_unit(self) -> str | None:
        """
        measurement unit is the unit the measurement value is to be interpreted as
        e.g. Volt, Ampere, Coloumb, ...
        """
        return None
