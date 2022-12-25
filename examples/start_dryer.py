import sys, os, yaml, webbrowser
from homeconnect import HomeConnect


def print_status(app):
    print(app.name)
    print(yaml.dump(app.status))


# Get credentials from environment variables
clientid = os.getenv("HomeConnect_ClientID", "")
clientsecret = os.getenv("HomeConnect_ClientSecret", "")
redirecturi = os.getenv("HomeConnect_RedirectURI", "")

# Set up HomeConnect object and authenticate
hc = HomeConnect(clientid, clientsecret, redirecturi)

if not hc.token_load():
    webbrowser.open(hc.get_authurl())
    auth_result = input("Please enter the URL redirected to: ")
    hc.get_token(auth_result)

# List appliances and their status
appliances = hc.get_appliances()
for app in appliances:
    try:
        app.get_status()
        print_status(app)
    except:
        pass

# Loop through appliances and start the first dryer we find
for app in appliances:
    if app.type == "Dryer":
        print(
            "This is the dryer. Let's see whether all conditions for remote start are met..."
        )
        conditions_met = True
        if (
            app.status["BSH.Common.Status.DoorState"]["value"]
            == "BSH.Common.EnumType.DoorState.Closed"
        ):
            print("Door: OK")
        else:
            conditions_met = False
            print(
                "Door: Not OK - " + app.status["BSH.Common.Status.DoorState"]["value"]
            )
        if (
            app.status["BSH.Common.Status.OperationState"]["value"]
            == "BSH.Common.EnumType.OperationState.Ready"
        ):
            print("State: OK")
        else:
            conditions_met = False
            print(
                "State: Not OK - "
                + app.status["BSH.Common.Status.OperationState"]["value"]
            )
        if app.status["BSH.Common.Status.RemoteControlActive"]["value"] == True:
            print("RemoteControlActive: OK")
        else:
            conditions_met = False
            print(
                "RemoteControlActive: Not OK - "
                + str(app.status["BSH.Common.Status.RemoteControlActive"]["value"])
            )
        if app.status["BSH.Common.Status.RemoteControlStartAllowed"]["value"] == True:
            print("RemoteControlAllowed: OK")
        else:
            conditions_met = False
            print(
                "RemoteControlAllowed: Not OK - "
                + str(
                    app.status["BSH.Common.Status.RemoteControlStartAllowed"]["value"]
                )
            )

        if conditions_met:
            print("Looking good - sending start command to dryer.")
            # Prepare data object to set up dryer program
            # Docs: https://api-docs.home-connect.com/programs-and-options?#dryer
            dataobj = {"data": {"key": "LaundryCare.Dryer.Program.Cotton"}}
            app.put(endpoint="/programs/active", data=dataobj)
        break
