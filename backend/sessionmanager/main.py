import sqlite3
import secrets
from google_api_token_getter.main import GoogleApiTokenGetter


class SessionManager:
    def __init__(self) -> None:
        self.gapi = GoogleApiTokenGetter(
            client_id="", client_secret="", redirect_uri="")

    def getAuthURL(self) -> str:
        return self.gapi.get_oauth_url()

    def getSessionToken(self) -> str:
        return secrets.token_hex()

    def getGoogleAPIToken(self, sessionToken) -> str:
        print(sessionToken)
        dbname = "sessionmanager/test.db"
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        line = c.execute(
            "select id,actoken from users where sstoken=?", [sessionToken]).fetchone()
        print(line)

        if line is None:
            print("data not found")
            # create actoken

            # gapi = GoogleApiTokenGetter()
            # accessToken = gapi.get_token()
            # add actoken sstoken
            accessToken = "ac4"
            c.execute("insert into users(actoken,sstoken) values(?,?)",
                      [accessToken, sessionToken])
            # return apitoken
            conn.commit()
            conn.close()
            return accessToken

        accessToken = line[1]
        if accessToken is None:
            # create actoken
            # add sstoken
            print(line[0])
            accessToken = "ac"
            c.execute("update users set actoken=? where id=?",
                      [accessToken, line[0]])
            conn.commit()

        conn.close()
        return accessToken


if __name__ == "__main__":
    sm = SessionManager()
    # sm.getGoogleAPIToken("ss2")
