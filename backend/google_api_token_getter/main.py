class GoogleApiTokenGetter:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_token(self, code: str) -> str:
        # Get token from Google API
        return "token"

    def get_oauth_url(self) -> str:
        # Get OAuth URL
        return "https://accounts.google.com/o/oauth2/auth?client_id={}&redirect_uri={}&response_type=code&scope=https://www.googleapis.com/auth/drive".format(
            self.client_id, self.redirect_uri
        )
