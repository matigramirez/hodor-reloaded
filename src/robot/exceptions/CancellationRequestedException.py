class CancellationRequestedException(Exception):
    def __init__(self):
        super().__init__("Cancelación solicitada por el usuario")
