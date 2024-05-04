import sqlite3
import secrets
import datetime
from google_api_token_getter.main import GoogleApiTokenGetter


class SessionManager:
    def __init__(self) -> None:
        self.gapi = GoogleApiTokenGetter(
            client_id="", client_secret="", redirect_uri="")

        dbname = "sessionmanager/test.db"
        self.conn = sqlite3.connect(dbname)
        self.c = self.conn.cursor()

    def getAuthURL(self) -> str:
        return self.gapi.get_oauth_url()

    def getSessionToken(self) -> str:
        return secrets.token_hex()

    def verifySessionToken(self, sessionToken) -> str:
        line = self.c.execute(
            "select expiry from users where sstoken=?", [sessionToken]).fetchone()

        now = datetime.datetime.now()

        if line is None:
            expiry = now + datetime.timedelta(days=14)
            expiry = expiry.strftime("%Y-%m-%d %H:%M:%S")
            self.c.execute("insert into users(sstoken,expiry) values(?,?)",
                           [sessionToken, expiry])
            self.conn.commit()
            return sessionToken

        if datetime.datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S') < now:
            return sessionToken

        self.c.execute("delete from users where sstoken=?", [sessionToken])
        newToken = self.getSessionToken()

        return newToken

    def getGoogleAPIToken(self, sessionToken) -> str:
        print(sessionToken)

        line = self.c.execute(
            "select id,actoken from users where sstoken=?", [sessionToken]).fetchone()
        print(line)

        """

        if line is None:
            print("data not found")
            # create actoken

            # gapi = GoogleApiTokenGetter()
            # accessToken = gapi.get_token()
            # add actoken sstoken
            accessToken = "ac4"
            expiry = ""
            self.c.execute("insert into users(actoken,sstoken,expiry) values(?,?,?)",
                      [accessToken, sessionToken, expiry])
            # return apitoken
            conn.commit()
            conn.close()
            return accessToken

        """

        accessToken = line[1]
        if accessToken is None:
            # create actoken
            # add sstoken
            print(line[0])
            accessToken = "ac"
            self.c.execute("update users set actoken=? where id=?",
                           [accessToken, line[0]])
            self.conn.commit()

        self.conn.close()
        return accessToken


if __name__ == "__main__":
    sm = SessionManager()
    # sm.getGoogleAPIToken("ss2")
