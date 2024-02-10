# Discord-Verify-Bot ✅
A bot designed to verify members and automatically re-add them to any server

# Discord Bot Setup

1. You'll need to go to the [Discord Devoloper Page](https://discord.com/developers/applications) and create a new application, and setup the OAuth with your server address, you may need to find a tutorial

2. Set the following env variables
    - `oauth_link` - The link for actually adding the application to your account, findable on the devoloper page 
    - `bot_link` - The link for actually adding the bot to your server, findable on the devoloper page
    - `client_secret` - Authorization token used for OAuth on discord, findable on the devoloper page
    - `client_id` - The identification number for your OAuth application, findable on the devoloper page
    - `token` - The actual bot token for the discord bot.

3. Make sure the bot has manage message permissions as well as send and read message. Also enable every single intent.

4. Then in the desired channel run `$create_verify <@role>` to create the verify message. Anyone who then runs the `$verify` command in your server will then recieve the role you created

# Commands ⚙

The commands are listed below:

`$join server_id amount/userid` - Will make users join the desired server from the server_id. You can either provide an amount of users to move or the specific userid as the second arguement

`$get_data` - Will send all server auth data to the channel of the message in a json file.