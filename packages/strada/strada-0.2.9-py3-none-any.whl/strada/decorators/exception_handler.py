import functools

from ..exception import StradaValidationException


def exception_handler(func):
    """A decorator to catch exceptions and create a standardized error message."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except StradaValidationException as e:
            class_name = self.__class__.__name__
            instance_name = getattr(self, "name", class_name)
            error_message = (
                f"[Error] {instance_name}.{func.__name__}:\n\t {with_indent(str(e))}"
            )
            print(error_message)
        except Exception as e:
            class_name = self.__class__.__name__
            instance_name = getattr(self, "name", class_name)
            error_message = (
                f"[Error] {instance_name}.{func.__name__}:\n\t {with_indent(str(e))}"
            )
            print(error_message)  # Or log the error message

    return wrapper


def with_indent(input_str):
    exception_message_lines = input_str.split("\n")
    indented_exception_message = "\n\t".join(exception_message_lines)
    return indented_exception_message
