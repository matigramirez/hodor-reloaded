class CancellationToken:
    def __init__(self):
        self.is_cancellation_requested = False

    def request_cancellation(self):
        self.is_cancellation_requested = True

    def reset(self):
        self.is_cancellation_requested = False
