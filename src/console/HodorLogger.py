from termcolor import colored


class HodorLogger:
    @staticmethod
    def init(message: str):
        print(colored(message, 'dark_grey'))

    @staticmethod
    def log(message: str):
        print(colored("[LOG] " + message, 'cyan'))

    @staticmethod
    def info(message: str):
        print(colored("[INF] " + message, 'blue'))

    @staticmethod
    def success(message: str):
        print(colored("[SUC] " + message, 'green'))

    @staticmethod
    def warning(message: str):
        print(colored("[WRN] " + message, 'yellow'))

    @staticmethod
    def error(message: str):
        print(colored("[ERR] " + message, 'red'))
