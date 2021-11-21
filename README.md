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