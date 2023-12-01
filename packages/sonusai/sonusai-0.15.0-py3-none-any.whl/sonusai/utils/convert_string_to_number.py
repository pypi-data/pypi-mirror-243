def convert_string_to_number(string: str) -> float | int | str:
    try:
        result = float(string)
        if result == int(result):
            return int(result)
        return result
    except ValueError:
        return string
