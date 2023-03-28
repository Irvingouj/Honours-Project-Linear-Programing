
class NoSolutionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UnboundedException(Exception):
    def __init__(self, *args: object,ray) -> None:
        self.ray = ray
        super().__init__(*args)

class ResultNotEqualException(Exception):
    def __init__(self, program,*args: object) -> None:
        self.program =program;
        super().__init__(*args)
    
class PerceptionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)