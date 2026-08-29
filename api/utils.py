from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        return response

    if isinstance(response.data, dict) and "detail" in response.data:
        response.data = {"message": str(response.data["detail"])}
    else:
        response.data = {"message": first_validation_error(response.data)}

    return response


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
