class UndesirableResultError(Exception):
    def __init__(self, result, desirable_result):
        self.result = result
        self.desirable_result = desirable_result

    def __str__(self):
        return f"{self.result} is undesirable, should be like {self.desirable_result}."
