class ReAuthentificationNeededException(Exception):
    def __init__(self, message="Token was expired. Please re-authenticate."):
        self.message = message
        super().__init__(self.message)