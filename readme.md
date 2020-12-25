# Tournament Management

This web application is created to make player registrations for a tournament easier, where a captain can create team 
and players can join in after captains approval. This web app is made to be hosted on Google App Engine, and uses 
Google Firestore. Login/ Registration is using Facebook and Steam (Only once) for fetching player data. 

## Register your application

- Register on [Google Cloud](https://console.cloud.google.com)
- Set-up Billing and create an account.
- Go to [Google Developers Console](https://console.developers.google.com/project) and create a new project. 
  This will automatically enable an App Engine application with the same ID as the project.
- Enable the "Google Cloud Datastore API" under "APIs & auth > APIs."


## Google App Engine
- Enable [App Engine API](https://console.developers.google.com/apis/api/appengine.googleapis.com/)
- Enable [Compute Engine API](https://console.developers.google.com/apis/api/compute.googleapis.com)
- Enable [Firestore API](https://console.cloud.google.com/marketplace/product/google/file.googleapis.com)
- Open [Google App Engine](https://console.cloud.google.com/appengine)
    - Create Application
    - Region as per requirement
    - Language: Python, Enviornment: Standard
    - Skip (I'll do this later)

- Start 
[Google Cloud Shell Editor](https://console.cloud.google.com/cloudshell/editor)
    - Clone this repository 
    - `$ cd <project-folder-name>`
    - `$ gcloud app deploy app.yaml --project <project-id>`

## Deploy to App Engine

**Deploy with gcloud**

```
$ gcloud config set project YOUR_PROJECT_ID
$ gcloud app deploy
```

## Configuration

File used to set configuration: **config_prod.conf**

- Name of your site, this will reflect on every page. Replace `Tournament Manager` 
with any name of your choice.
```
DISPLAY_NAME = Tournament Manager
```

- Fixtures link to redirect to for match fixtures. Provide any external link of 
fixtures in place of `#`.
```
$FIXTURES_LINK = '#';
```

- Google Cloud Project ID for App Engine. Enter the ID you got while 
[Register your application](#register-your-application) step.
```
PROJECT_ID = 
```

- Insert your Steam WebAPI-Key, it can found at 
[Steam API Key](https://steamcommunity.com/dev/apikey). Login with your steam 
credentials for generating a key.
```
STEAM_API_KEY = 
```

- Insert your Facebook Developer API key. You can create one at
[Facebook for Developers](https://developers.facebook.com).
Go to `My Apps -> Add new App` to create a new app and get its app ID
```
FACEBOOK_API_KEY = 
```

- This is used to set Maximum players allowed in a team.
```
MAX_PLAYERS = 7
```

- This is used to set the mode in which the web application will work.
Different modes are given below.
    - 1 -> Normal Team mode
    - 2 -> Registrations closed for team mode
    - 9 -> Registrations closed for team mode with no changes in team
```
MODE = 1
```

## Sample Web Application

Sample web application for Tournament Management can be found at
[Tourney Manager](https://narcotic-gaming-ncl.appspot.com/).