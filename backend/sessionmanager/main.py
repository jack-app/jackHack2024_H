import sqlite3


class SessionManager:
    def __init__(self) -> None:
        pass

    def getAuthURL(self):
        pass

    def getSessionToken(self):
        pass

    def getGoogleAPIToken(self, sessionToken):
        # if sessionToken in db return apitoken
        # else create apitoken

        dbname = 'test.db'
        conn = sqlite3.connect(dbname)
        c = conn.cursor()

        line = c.execute(
            f"select actoken from users where sstoken=?", [sessionToken]).fetchone()

        if line is None:
            print("data not found")
            # create actoken
            # add actoken sstoken
            # return apitoken

        accessToken = line[0]
        if accessToken is None:
            # create actoken
            # add sstoken
            # return actoken
            pass

        return accessToken


if __name__ == "__main__":
    sm = SessionManager()
    sm.getGoogleAPIToken("ss1")
