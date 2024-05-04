import requests


class GoogleApiTokenGetter:
    # def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
    #     self.client_id = client_id
    #     self.client_secret = client_secret
    #     self.redirect_uri = redirect_uri

    def __init__(self):
        self.client_id = "client_id"
        self.client_secret = "client_secret"
        self.redirect_uri = "redirect_uri"

    def get_token(self, code: str) -> str:
        url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
        }
        response = requests.post(
            url,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        return response.json()

    def get_oauth_url(self) -> str:
        # Get OAuth URL
        return "https://accounts.google.com/o/oauth2/auth?client_id={}&redirect_uri={}&response_type=code&scope=https://www.googleapis.com/auth/drive".format(
            self.client_id, self.redirect_uri
        )
