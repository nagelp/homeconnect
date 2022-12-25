import sys, os, yaml, webbrowser
from homeconnect import HomeConnect


def print_status(app):
    print(app.name)
    print(yaml.dump(app.status))


clientid = os.getenv("HomeConnect_ClientID", "")
clientsecret = os.getenv("HomeConnect_ClientSecret", "")
redirecturi = os.getenv("HomeConnect_RedirectURI", "")

hc = HomeConnect(clientid, clientsecret, redirecturi)

if not hc.token_load():
    webbrowser.open(hc.get_authurl())
    auth_result = input("Please enter the URL redirected to: ")
    hc.get_token(auth_result)

appliances = hc.get_appliances()

# List appliances
for app in appliances:
    try:
        app.get_status()
        print_status(app)
    except:
        pass

# Prepare data object to set up dryer program
# Docs: https://api-docs.home-connect.com/programs-and-options?#dryer
dataobj = {"data": {"key": "LaundryCare.Dryer.Program.Cotton"}}

# Loop through appliances and start the first dryer we find
# with the chosen program above
for app in appliances:
    if app.name == "Dryer":
        print("This is the dryer. Let's start it.")
        app.put(endpoint="/programs/active", data=dataobj)
        break
