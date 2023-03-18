
class NoSolutionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ResultNotEqualException(Exception):
    def __init__(self, program,*args: object) -> None:
        self.program =program;
        super().__init__(*args)
