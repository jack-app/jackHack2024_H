if __name__ == "__main__":
    from google_api_token_getter.main import GoogleApiTokenGetter

    google_api_token_getter = GoogleApiTokenGetter()

    print(google_api_token_getter.get_oauth_url())
