"""
🔄 Wrap Around
"""


def wrap_value(value, min_val, max_val):
    range_val = max_val - min_val
    if range_val <= 0:
        return min_val
    return ((value - min_val) % range_val) + min_val


def wrap_y(y, height=1920):
    return wrap_value(y, 0, height)


def wrap_x(x, width=1080):
    return wrap_value(x, 0, width)
