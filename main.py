import discord
import os
# import datetime
import asyncio
# import requests, json
client = discord.Client()


@client.event
async def on_ready():
  	print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
		if message.author == client.user:
			return
		if message.channel.id == 795638996381990972:
			if message.content.startswith("Name:"):
				await applicationcheck(message)
		elif message.content.startswith("r!"):
			if message.content.startswith("r!ban"):
				await ban(message)
			elif message.content.startswith("r!kick"):
				await kick(message)
			else: 
				await message.channel.send("`Invalid command run r!help to view the valid commands`")

async def applicationcheck(message):
	await message.add_reaction("✅")
	await message.add_reaction("❌")
	if "Revelation Council" in str(message.role_mentions):
		return
	else:
		revc = message.guild.get_role(795652505613631499)
		await message.channel.send(revc.mention +" somebody screwed up their application and forgot to ping")

async def kick(message):
	if len(message.mentions) == 1:
		params = str.split(message.content)
		usr = message.mentions[0]
		if len(params) == 1:
			await message.guild.kick(usr, "Reason was not specified - " + message.author.name)
			await message.channel.send("`"+ usr.name + "has been successfully kicked" + "`")
		elif len(params) >= 2:
			await message.guild.kick(usr, params[2:])
			await message.channel.send("`"+ usr.name + "has been successfully kicked" + "`")

async def ban(message):
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

@client.event
async def on_member_join(user):
		global lastjoin
		lastjoin = str(user.id)

client.run(os.getenv("token"))