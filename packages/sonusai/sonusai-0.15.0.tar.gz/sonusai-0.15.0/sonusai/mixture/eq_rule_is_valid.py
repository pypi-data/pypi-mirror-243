from typing import Any


def eq_rule_is_valid(rule: Any) -> bool:
    """Check if EQ rule is valid

    An EQ rule must be a tuple of length 3 or a list of length 3 tuples.
    """

    # Must be a list
    if not isinstance(rule, list):
        return False

    if len(rule) != 3:
        # If the length is not 3, then all elements must also be lists
        if not all(isinstance(el, list) and len(el) == 3 for el in rule):
            return False
        rules = rule
    else:
        rules = [rule]

    for r in rules:
        # Each item must be a number or string
        if not all(isinstance(el, float | int | str) for el in r):
            return False

        for el in r:
            # If a string, item must start with 'rand'
            if isinstance(el, str) and not el.startswith('rand'):
                return False

    return True
