import discord
import os
# import datetime
import asyncio
# import requests, json
client = discord.Client()
serverid = 426488629788016640
logsid = 795753613396803635


@client.event
async def on_ready():
  	print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
		if message.author == client.user:
			return
		if message.channel.id == 795638996381990972:
			if message.content.startswith("Name:"):
				await message.add_reaction("✅")
				await message.add_reaction("❌")
				if "Revelation Council" in str(message.role_mentions):
					return
				else:
					revc = message.guild.get_role(795652505613631499)
					await message.channel.send(revc.mention +" somebody screwed up their application and forgot to ping")
		elif message.content.startswith("r!"):
			if message.content.startswith("r!ban"):
				if len(message.mentions) == 1:
					params = str.split(message.content)
					print("Count: " + str(len(params)))
					usr = message.mentions[0]
					if len(params) == 2:
						if str.isnumeric(params[2]):
							await message.guild.ban(usr, "No reason was input - " + message.author.name, delete_message_days=int(params[2]))
							await message.channel.send("`"+ usr.name + " has been banned successfully" + "`")
					elif len(params) >= 3:
							await message.guild.ban(usr, reason=str(params[3:]) + " - " + message.author.name, delete_message_days=str(params[2]))
							await message.channel.send("`"+ usr.name + " has been banned successfully" + "`")
					else:
						await message.guild.ban(usr, reason="No reason was input - "+ message.author.name, delete_message_days=0)
						await message.channel.send("`"+ usr.name + " has been banned successfully" + "`")
				else:
					await message.channel.send("""Improper use of ban command
					`r!ban @user, 0-7 amount of days to delete messages from, reason for ban""")
			elif message.content.startswith("r!kick"):
				if len(message.mentions) == 1:
					params = str.split(message.content)
			else: 
				return
		else:
			return

#invites = {}
#lastjoin = ""


@client.event
async def on_member_join(user):
		global lastjoin
		lastjoin = str(user.id)


"""" #shut up its not stolen code that doesnt even work
async def fetch():
    global lastjoin
    global invites
    await client.wait_until_ready()
    gld = client.get_guild(int(serverid))
    logs = client.get_channel(int(logsid))
    while True:
        invs = await gld.invites()
        tmp = []
        for i in invs:
            for s in invites:
                if s[0] == i.code:
                    if int(i.uses) > s[1]:
                        usr = gld.get_member(int(lastjoin))
                        testh = f"{usr.name} **joined**; Invited by **{i.inviter.name}** (**{str(i.uses)}** invites)"
                        await logs.send(testh)
            tmp.append(tuple((i.code, i.uses)))
        invites = tmp
        await asyncio.sleep(4)
client.loop.create_task(fetch())"""


client.run(os.getenv("token"))