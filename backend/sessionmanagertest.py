from sessionmanager.main import SessionManager

sm = SessionManager()
sessionToken = "ss2"  # sm.getSessionToken()
token = sm.getGoogleAPIToken(sessionToken)
print(token)
