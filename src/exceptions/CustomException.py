from sys import exc_info as sys

def error_message_details(error, exc_info):
    exc_type, exc_value, exc_tb = exc_info.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"Error occurred in Python Script named [{file_name}] at line number [{line_number}] error_message [{error}]"
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, exc_info=None) -> None:
            super().__init__(error_message)
            if exc_info:
                self.error_message = error_message_details(error_message, exc_info)
            else:
                self.error_message = error_message

    def __str__(self) -> str:
        return self.error_message
