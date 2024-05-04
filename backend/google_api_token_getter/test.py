import os

import dotenv

if __name__ == "__main__":
    import main

    dotenv.load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI")
    code = os.getenv("CODE")

    google_api_token_getter = main.GoogleApiTokenGetter(
        client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri
    )

    print(google_api_token_getter.get_token(code=code))
    # print(google_api_token_getter.get_oauth_url())
