import threading, tempfile, asyncio, discord, random, json, time, api, os
from discord.ext.commands import has_permissions
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix="$", description="Desc", intents=discord.Intents.all())
auth_link = os.environ['oauth_link']

@bot.event
async def on_ready():
    print("Bot has successfully logged in as: {}".format(bot.user))

@bot.command()
@has_permissions(administrator=True)
async def create_verify(ctx, role : discord.Role):
    guild = str(ctx.guild.id)
      
    view = discord.ui.View()
    button = discord.ui.Button(label="Verify", url=auth_link, style=discord.ButtonStyle.success)
    view.add_item(button)
    embed = discord.Embed(title="Verification", description="Click the button below to verify", color=0x7289da)
    embed.set_image(url="https://i.gifer.com/67Kr.gif")

    guild_file = json.load(open('guilds.json', 'r+'))

    if not guild in guild_file:
      guild_file[guild] = {}
  
    guild_file[guild]['role_id'] = role.id

    with open("guilds.json", "w+") as file:
      json.dump(guild_file, file, indent=2)

    await ctx.send(embed=embed, view=view)

@bot.command()
async def verify(ctx):
    guild_file = json.load(open("guilds.json", "r+"))
    guild = str(ctx.guild.id)  
    id = str(ctx.message.author.id)
    
  
    role = get(ctx.guild.roles, id=guild_file[guild]['role_id'])
    

    auth_file = json.load(open("auths.json", "r+"))
  
    if not id in auth_file:
      await ctx.send('You have not verifiied your account yet.')

    else:
      await ctx.message.author.add_roles(role)
      await ctx.message.delete()
      await ctx.send('You have been verified!', delete_after=5)


    guild_file[guild][id] = auth_file[id]
      
    with open("guilds.json", "w+") as file:
      json.dump(guild_file, file, indent=2)
    
      

@bot.command()
@has_permissions(administrator=True)
async def join(ctx, guild, amount=0, admin=False):
    guild = str(ctx.guild.id)
  
    if (admin):
        guild_file = json.load(open("auths.json", "r+"))
        print(guild_file)
    else:

        guild_file = json.load(open("guilds.json", "r+"))
        if not guild in guild_file:
          await ctx.send("You haven't setup your server yet! Use `$create_verify <@role>` to setup your server.")
          return
        else:
          guild_file = guild_file[guild]
          del guild_file['role_id']
          
    await ctx.send("Please be patient...")

      
    for id in list(guild_file.keys())[:amount]:
        if amount > 10**7:
            id = str(amount)
          
        data =  guild_file[id]
        auth = data[0]

        print(id)
      
        try:
            api.add_to_guild(auth, id, int(guild))
        except:
            time.sleep(10)
            try:
                code = api.refresh_token(data[1])
                code['access_token']
            except:
                del guild_file[id]
                continue
            
            guild_file[id] = [code['access_token'], code['refresh_token']]
            api.add_to_guild(code['access_token'], id, int(guild))
      
            with open("auths.json", "w+") as file:
                json.dump(guild_file, file, indent=2)

        if amount > 10**7:
            break
      
    await ctx.send("**Done! ✅**")

@bot.command()
@has_permissions(administrator=True)
async def get_data(ctx, guild=None, admin=False):

    if (admin):
        guild_file = json.load(open("auths.json", "r+"))
    else:
        guild_file = json.load(open("guilds.json", "r+"))
        guild_file = guild_file[str(ctx.guild.id)]
        del guild_file['role_id']

    
    with open("auth_data.json", "w+") as file:
      json.dump(guild_file, file, indent=2)
      
    await ctx.send('Data served. The first item in the list is the active token, and the second is the refresh.\n\n**WARNING** :warning:Improper usage may lead to the auths not working with Flow Bot :warning:\nRead the docs and dont use the refresh token first to create a new auth just to be safe.', file=discord.File('auth_data.json'))
  
def run():
  bot.run(os.environ['token'])