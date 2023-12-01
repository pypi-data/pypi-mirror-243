def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer
    for element in it:
        value = function(value, element)
    return value


def clearConsole():
    print("\033c", end='')

def clamp(v: float, len:int = 2):
    return float(("{:."+str(len)+"f}").format(v))