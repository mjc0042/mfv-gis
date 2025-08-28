""" Module for utiliy functions """

def get_numeric_value(value) -> int | float:
    """ Converts value to int or float """

    if not value:
        return None
    try:
         # Try convert to int first if it's an int or string representing int
        if isinstance(value, (int, float)):
            # If float but represents whole number, convert to int
            if isinstance(value, float) and value.is_integer():
                return int(value)
            else:
                return float(value)  # float stays float
        else:
            # Try int conversion for strings of integers
            return int(value)
    except (TypeError, ValueError):
        return None
