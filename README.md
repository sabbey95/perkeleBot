# Perkele Bot

Slack bot to berate people who take too long to respond to civ turn requests.

## Run locally

To install dependencies run:-

```bash
pip3 install -r ./requirements.txt 
```

To run locally you need a slack environment with the bot set up. Create a .env file in the folder root with the
following format:-

```dotenv
SLACK_TOKEN=
SIGNING_SECRET=
DATABASE_URL=sqlite:///database.db?check_same_thread=False
```

The SLACK_TOKEN and SIGNING_SECRET can be found slack workspace settings when setting up the bot.

Then just run ```app.py```
The app will run locally on port 5000, you can use ngrok to set up a temporary url for slack to hit with requests.
Install ngrok and run

```bash
path_to_ngrok/ngrok http 5000
``` 

Use the url this creates on the slack api website when setting up the bot.