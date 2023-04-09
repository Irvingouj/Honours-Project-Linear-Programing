
class NoSolutionException(Exception):
    def __init__(self, *args: object,stage ,constraints = None,three_d_bound_certificate = None) -> None:
        self.stage = stage
        self.three_d_bound_certificate = three_d_bound_certificate
        self.constraints = constraints
        super().__init__(*args)

class UnboundedException(Exception):
    def __init__(self, *args: object,unbounded_certificate, unbounded_index) -> None:
        self.unbounded_certificate = unbounded_certificate
        self.unbounded_index = unbounded_index
        super().__init__(*args)

class ResultNotEqualException(Exception):
    def __init__(self, program,*args: object) -> None:
        self.program =program;
        super().__init__(*args)
    
class PerceptionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AbnormalException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)