import requests

print("confirm that FASTAPI server is running on localhost:8000\n")
print("If not, type `uvicorn main:app --reload`.")

authFlowState = requests.get("http://localhost:8000/getAuthFlowState")

print(authFlowState.json()["auth_url"])
print(authFlowState.cookies)
print("please access the url above and get the code from the redirected url.")

input("press enter to continue...")

tokens = requests.get("http://localhost:8000/getTokens",cookies=authFlowState.cookies.get_dict())

print(tokens.json())
print(tokens.cookies)