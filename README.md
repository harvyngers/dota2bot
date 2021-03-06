# Dota2HelperBot, a Discord bot to give live updates on Dota 2 tournament games and more

Dependencies:
* Python >=3.5
* discord.py

Get Python here: https://www.python.org/downloads/

For more information on installing discord.py, go here: https://github.com/Rapptz/discord.py

To use this bot, you need to create a file named "settings.json" in the data/ folder, like so:

```
{
	"token": <your token here>
	"apikey": <your Steam user API key here>
}
```

In order to obtain a token, create a new bot user here: https://discordapp.com/developers/applications/me

In order to obtain a Steam user API key, go here: https://steamcommunity.com/dev/apikey

The complete list of options is as follows:
```
{
	"token": String that will be the bot's token
	"prefix": String representing the command prefix, defaults to ;
	"owner": String representing your Discord user ID
	"changenick_interval": Int, number of seconds to wait before changing nickname again, default: 600
	"api_interval": Int, number of seconds to wait before making another call to Valve's API (recommended to be greater than 1), default: 20
	"apikey": String representing your Steam API key
	"filter_matches": Bool, determines whether the bot only reports on important matches (i.e. matches in notable leagues), default: true
	"notable_leagues": Array of ints representing the IDs of leagues you want to track. default: [5401] (see Tips)
	"filter_generic": Bool, determines whether the bot filters out matches where neither team has a real name, default: true
	"no_repeat_matches": Bool, controls whether the bot filters out matches with the same teams and series score as a previous one, default: true
	"save_match_data": Bool, controls logging of data obtained from API calls, default: false
	"verbose": Bool, enables a bit more information in the program output, default: true
}
```

Of these fields, only `token` and `apikey` are required. The bot will attempt to determine its owner automatically if `owner` is not provided.

## Implemented commands

`changename` - Causes the bot to choose a random new nickname.

`join` - Displays a link where server owners can add this bot.

`ongoing` - Shows matches that are currently being “tracked” by the bot.

`leagues` - Shows the list of notable leagues.

`welcomechannel` - Sets the channel for posting welcome messages. When used without an argument, shows current setting. Otherwise, accepts a channel mention, a channel name, or a channel ID.

`matchchannel` - Sets the channel for posting match updates. When used without an argument, uses the current channel. Otherwise, accepts a channel mention, a channel name, or a channel ID.

`welcome` - Turns the welcome messages on or off. When used without an argument, shows current setting. Use "off", "no", or "false" to turn welcome messages off. Anything else turns it on.

`victorymessages` - Turns the victory messages on or off. When used without an argument, shows current setting. Use "off", "no", or "false" to turn victory messages off. Anything else turns it on.

`showresult` - Controls whether the bot displays the winner, duration, and final score in the victory message. When used without an argument, shows current setting. Use "off", "no", or "false" to turn this option off. Anything else turns it on.

`contact` - Sends a message to the bot owner. Has a cooldown of 60 seconds.

`untrack` - Removes all matches from the tracking list. Can only be used by the bot owner. Note that if this is called while any tracked matches are going on, they will probably be added right back to the list on the next API call!

`addleague` - Adds to the list of notable leagues. Can only be used by the bot owner. Does not currently affect the notable_leagues field in settings.json, so any changes made using this command are not persistent between restarts.

`rmleague` - Removes from the list of notable leagues. Can only be used by the bot owner. Does not currently affect the notable_leagues field in settings.json, so any changes made using this command are not persistent between restarts.

`autochangename` - Turns the nickname changing feature on or off. When used without an argument, shows current setting. Use "off", "no", or "false" to turn the nickname changing off. Anything else turns it on. Setting this option to false will also reset the bot's nickname.

`globalnamereset` - Resets the bot's nickname in all servers. Can only be used by the bot owner. This command should rarely be used.

`faq` - Displays a basic FAQ.

Any action that changes a server-specific setting must be performed by a server admin or the bot owner.

## Unimplemented commands

`status` - Shows the game state of all currently tracked matches.

`predict radiant|dire` - Sets your prediction for the specified team.

`score` - Shows the given user’s prediction record.

`restart` - Restarts the bot. Can only be used by the bot owner.

`reload` - Reloads all cogs. Can only be used by the bot owner.

`servers` - Shows all the servers the bot is connected to.

## Tips

* I recommend that you set the PYTHONIOENCODING environment variable to utf-8 in order to give the program an easier time when trying to print team names with special characters, especially in verbose mode. On Linux, try `export PYTHONIOENCODING="utf-8"`. On Windows, try `set PYTHONIOENCODING="utf-8"`.
* Valve's API occasionally sends multiple matches with the same data but different match IDs. Although the bot should filter out the duplicates (with no_repeat_matches enabled), it will still track all of them, since it has no way of knowing which is the "real" one. After a while, there might be a slowly growing pile of duplicate matches that will never finish. Therefore, it's a good idea to run `ongoing` (to make sure no real matches are going on) and `untrack` from time to time to clean them up. In the future the program will be able to clean up these duplicates automatically.\

## FAQ

**Why am I not getting updates for matches?**

Make sure a channel is set through the `;matchchannel` command. Also, make sure you've given the bot permissions to talk in that channel.

**What's with the nicknames? Can I set my own nickname for the bot?**

If the `autochangename` setting is on, the bot will automatically change its name periodically to the name of a random Dota 2 bot. To set your own nickname for the bot, disable `autochangename` and then right-click the bot and select "Change Nickname".

**Will you periodically add new leagues to the bot?**

I will on my instance of the bot. If you're running your own instance of the bot, you'll have to add new leagues through the `;addleague` command or by editing the settings.json file.

**How do I find out what ID a tournament comes under?**

You can get league IDs by calling Valve's API (https://api.steampowered.com/IDOTA2Match_570/GetLeagueListing/v1/?key=YOUR_API_KEY). In the future I hope to have some way to let people know the league IDs of upcoming tournaments more easily.

## Todo

* Suppress first round of announcements (this is to avoid repeating announcements for ongoing matches if the bot is restarted)
* Add proper error handling if the bot does not have permissions to talk
* Implement unimplemented commands
* Implement subcommands
* Twitch streams
* Fetch and save kill score and net worth difference periodically
* Auto de-duplication

Check @Dota2HelperBot on Twitter for development news and updates
