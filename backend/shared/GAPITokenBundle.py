class GAPITokenBundle:
    def __init__(self, access_token: str, refresh_token: str, expires_at: float):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at