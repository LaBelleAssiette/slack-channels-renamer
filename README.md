# Slack channels renamer

Slack doesn't allow anymore to rename channels without an Entreprise token. It's behing the `admin` scopes. With a bot token, it can only rename channels that it owns basically.

The `main.py` script counters that by using a user token from the web app.

## Getting the token

* Inspect the slack web app
* Find a request to the slack API
* Get the "token" data in the multipart / get params and store it in `.env`
* Get the `d` cookie value and store it in `.env`

## `.env`

Parameters are set with a `.env` file. An example is provided below.

```
SLACK_COOKIES_D=cookie
SLACK_TOKEN=xoxc-token
SLACK_DOMAIN=example.slack.com
```

## Renaming

After running the script a first time, a `channels.json` state file is created. Modify this file by adding a `rename` field to the channels you'd like to rename.

Comment the call to `refresh_channels`. Otherwise the modification you have made would be overwritten.

Run `main.py` again. The channels are renamed.
