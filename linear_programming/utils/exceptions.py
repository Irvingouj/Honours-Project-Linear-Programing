
from typing import Tuple


class NoSolutionException(Exception):
    def __init__(self, *args: object, stage, constraints=None, three_d_bound_certificate=None) -> None:
        self.stage = stage
        self.three_d_bound_certificate = three_d_bound_certificate
        self.constraints = constraints
        super().__init__(*args)


class UnboundedException(Exception):
    def __init__(self, *args: object, stage: str) -> None:
        self.stage = stage
        super().__init__(*args)


class ResultNotEqualException(Exception):
    def __init__(self, program, *args: object) -> None:
        self.program = program
        super().__init__(*args)


class PerceptionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnboundedException2D(UnboundedException):
    def __init__(self, *args: object, stage: str, unbounded_index: int) -> None:
        super().__init__(*args, stage=stage)
        self.unbounded_index = unbounded_index


class UnboundedException3D(UnboundedException):
    def __init__(self, *args: object, stage: str, unbounded_index: Tuple[int, int]) -> None:
        super().__init__(*args, stage=stage)
        self.unbounded_index = unbounded_index

class NoSolutionException1D(NoSolutionException):
    def __init__(self, *args: object, stage: str) -> None:
        super().__init__(*args, stage=stage)

class NoSolutionException2D(NoSolutionException):
    def __init__(self, *args: object, stage: str, three_d_bounded_certificate=Tuple[int, int, int]) -> None:
        super().__init__(*args, stage=stage)
        self.three_d_bound_certificate = three_d_bounded_certificate


class NoSolutionException3D(NoSolutionException):
    def __init__(self, *args: object, stage: str) -> None:
        super().__init__(*args, stage=stage)


class AbnormalException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
