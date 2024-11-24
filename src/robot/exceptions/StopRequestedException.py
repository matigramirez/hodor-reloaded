class StopRequestedException(Exception):
    def __init__(self):
        super().__init__("Detenimiento solicitado por el usuario")
