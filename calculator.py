import math

def calculate_expression(expression, angle_mode="DEG"):
    expr = expression.replace("^", "**").strip()
    if not expr:
        return ""

    # تحويل الزوايا لو الوضع بالدرجات
    if angle_mode == "DEG":
        sin_fn = lambda x: math.sin(math.radians(x))
        cos_fn = lambda x: math.cos(math.radians(x))
        tan_fn = lambda x: math.tan(math.radians(x))
    else:
        sin_fn = math.sin
        cos_fn = math.cos
        tan_fn = math.tan

    allowed_names = {
        "sin": sin_fn,
        "cos": cos_fn,
        "tan": tan_fn,
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
        "exp": math.exp,
        "abs": abs,
        "pi": math.pi,
        "e": math.e,
    }

    try:
        # منع استخدام أي دوال خارج القائمة المسموحة
        result = eval(expr, {"__builtins__": None}, allowed_names)
        if isinstance(result, float):
            result = round(result, 10)
        return str(result)
    except Exception:
        return "Error"
