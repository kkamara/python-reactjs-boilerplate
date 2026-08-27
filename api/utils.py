def first_validation_error(errors):
    if isinstance(errors, dict):
        for value in errors.values():
            result = first_validation_error(value)
            if result is not None:
                return result
        return None

    if isinstance(errors, list):
        for item in errors:
            result = first_validation_error(item)
            if result is not None:
                return result
        return None

    return str(errors)
