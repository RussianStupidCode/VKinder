from app.frontend.console import config


def except_input_wrapper(error_message=None):
    """
    Зацикливание ввода пока не будет дан корректный ввод
    """
    def input_wrapper(function):
        def wrapper(*args, **kwargs):
            is_exit = False
            result = None
            while not is_exit:
                try:
                    result = function(*args, **kwargs)
                    break
                except Exception as e:
                    if error_message is None or config.DEBUG:
                        print(e)
                    else:
                        print(error_message)
            return result
        return wrapper
    return input_wrapper


def get_user_input(message):
    """
        Зацикливание ввода пока не будет дан непустой ввод
    """
    string = ''
    while not string:
        string = input(f'{message}: ').strip()
    return string
