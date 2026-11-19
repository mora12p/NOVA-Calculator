
from calculator import NovaCalculator

calc = NovaCalculator()

tests = [
    "5 + 10",
    "sqrt(25)",
    "sin(pi / 2)",
    "2^8",
    "log(100, 10)",
]

for expression in tests:
    try:
        result = calc.calculate(expression)
        print(f"{expression} = {result}")
    except ValueError as error:
        print(error)
