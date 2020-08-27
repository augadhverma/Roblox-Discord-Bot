# Roblox-Discord Bot
[![Support Server](https://cdn.discordapp.com/attachments/702180216533155936/748419162895810610/white_logo.png)](https://discord.gg/CTuUKJJ)

## About

A self-hostable bot to manage your Roblox group from your Discord!
___
## Requirements

- Python 3.7 or later
- [robloxapi](https://pypi.org/project/robloxapi/)

>⚠ Note: I highly suggest you to use the latest version of python available
___
## Installing and Setup

1. Clone this repo - `git clone https://https://github.com/ItsArtemiz/Roblox-Discord-Bot`

2. Navigate into the file [main.py](https://github.com/ItsArtemiz/Roblox-Discord-Bot/blob/master/main.py)

3. In `main.py` file replace the following:

```python
defaultprefix = ';' #change the prefix to whatever you want
defaultcolour = 0xcdcdcd #change to the hex code of your liking

client= robloxapi.Client("Your Roblox Cookie")
#Change to your roblox client cookie

owner=[371019056419045376,449897807936225290] # Replace discord ids of user who will have owner control over the bot, i.e, can use commands like setrank or shout

maingroup = 0000000 #Roblox Id of your main group

TOKEN = "Your Bot Token"

#Don't share your token with anyone. Tokens are like a password to the bot. If someone has your token, they have full control over your bot.
```
___
## Commands


- groupinfo 
- serverinfo
- account-info
- setrank
- invite
- echo
- gamepasses
- choose
- botinfo
- shout
- slap
- uptime
- roblox-info
- source
- exile
- verify
- avatar
- membercount
- help
- ping
- dice
- userinfo

---
## Features

### Hiding Commands in the help command (But the command still works)


- In order to hide a command from being displayed in the default help message, simply change `hidden=False` to `hidden=True`
---
### Getting stats of your Main Group

- After setting `maingroup` to your main group's id, simply run `groupinfo` command and it will show all the necessary stats about your group
---
### Getting stats on a user who is in your group

- If you want to check stats on a particular user who is in your group, run `roblox-info [member]` and it will show the following stats for the user: 

1. Role of the user in the group
2. Users pertaining to that role
3. Rank of the role (int: 1-255)


>⚠ Note: The user must be verified with the [API](https://verify.eryn.io)

---
### Getting gamepasses pertaining to a user

- To get all the gamepasses of a user, run `gamepasses [member]`

>⚠ Note: The user must be verified with the [API](https://verify.eryn.io)
___
## Support

If you have any suggestion or want to report a bug, join the support server: https://discord.gg/CTuUKJJ

___
## Roadmap

- Add binds
- Add moderation commands
- Better configuration