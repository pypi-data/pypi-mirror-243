class AirfoldError(Exception):
    pass


class AirfoldKeyError(AirfoldError, KeyError):
    pass


class AirfoldTypeError(AirfoldError, TypeError):
    pass


class MethodNotImplementedError(AirfoldError, NotImplementedError):
    pass
