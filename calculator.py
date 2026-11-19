
import ast
import operator
import sympy as sp


class NovaCalculator:

    FUNCTIONS = {
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "sqrt": sp.sqrt,
        "log": sp.log,
        "ln": sp.log,
        "exp": sp.exp,
        "abs": sp.Abs,
    }

    CONSTANTS = {
        "pi": sp.pi,
        "e": sp.E,
    }

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
    }

    def calculate(self, expression, angle_mode="RAD"):
        try:
            expression = expression.replace("^", "**").strip()

            if not expression or len(expression) > 200:
                raise ValueError("Invalid expression")

            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body, angle_mode)

            if result.free_symbols:
                raise ValueError("Variables are not supported")

            return sp.N(result)

        except Exception as error:
            raise ValueError("Invalid mathematical expression") from error

    def _evaluate(self, node, angle_mode):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return sp.sympify(node.value)
            raise ValueError("Invalid number")

        if isinstance(node, ast.Name):
            if node.id in self.CONSTANTS:
                return self.CONSTANTS[node.id]
            raise ValueError("Unknown constant")

        if isinstance(node, ast.BinOp):
            operation = self.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Unsupported operator")

            left = self._evaluate(node.left, angle_mode)
            right = self._evaluate(node.right, angle_mode)

            if isinstance(node.op, ast.Pow):
                if right.is_number and abs(float(right)) > 100:
                    raise ValueError("Exponent is too large")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            value = self._evaluate(node.operand, angle_mode)

            if isinstance(node.op, ast.USub):
                return -value

            if isinstance(node.op, ast.UAdd):
                return value

            raise ValueError("Unsupported operation")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function")

            name = node.func.id

            if name not in self.FUNCTIONS:
                raise ValueError("Unknown function")

            if node.keywords:
                raise ValueError("Invalid arguments")

            args = [
                self._evaluate(arg, angle_mode)
                for arg in node.args
            ]

            if name in ("sin", "cos", "tan") and angle_mode == "DEG":
                args[0] = args[0] * sp.pi / 180

            return self.FUNCTIONS[name](*args)

        raise ValueError("Unsupported expression")
