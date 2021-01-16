import discord
from discord.ext import commands
import os
from replit import db
MsgMute 
TotalMute
VCMute
hasMsgMute = False
hasTotalMute = False
hasVCMute = False

bot = commands.Bot(command_prefix="r!")
test = 426488629788016640

@bot.event
async def on_ready():
	print("Logged in as {0.user}".format(bot))
	guild = bot.get_guild(test)
	await checkmute(guild)

@bot.event
async def on_message(message):
		if message.author == bot.user:
			return
		elif message.channel.id == 795638996381990972:
			if message.content.startswith("Name:"):
				await applicationcheck(message)
		else:
			await bot.process_commands(message)

async def applicationcheck(message):
	await message.add_reaction("✅")
	await message.add_reaction("❌")
	if "Revelation Council" in str(message.role_mentions):
		return
	else:
		revc = message.guild.get_role(795652505613631499)
		await message.channel.send(revc.mention +" somebody screwed up their application and forgot to ping")


def checkperms(ctx, perm):
	usr = ctx.author
	perms = usr.guild_permissions
	if getattr(perms, perm) == True:
		return True
	else:
		ctx.send("`You don't have permission to run this command. Missing the " + perm + " permission`")
		return False

@bot.command()
async def kick(ctx):
	message = ctx.message
	if checkperms(ctx, "kick_members"):
		if len(message.mentions) == 1:
			params = str.split(message.content)
			usr = message.mentions[0]
			if len(params) == 1:
				await message.guild.kick(usr, "Reason was not specified - " + message.author.name)
				await message.channel.send("`"+ usr.name + "has been successfully kicked" + "`")
			elif len(params) >= 2:
				await message.guild.kick(usr, params[2:])
				await message.channel.send("`"+ usr.name + "has been successfully kicked" + "`")
			else:
				await message.channel.send("`Invalid parameters of kick [@user, reason] refer to r!help")
		else:
			await ctx.send("`You need to tag a user inorder to use this command!`")

@bot.command()
async def ban(ctx):
	if checkperms(ctx, "ban_members"):
		message = ctx.message
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
			await message.channel.send("""Improper use of ban command:	
`r!ban @user, 0-7 amount of days to delete messages from, reason for ban`""")

@bot.command()
async def mute(ctx, user, time, *reason):
	print("a")

@bot.event
async def on_guild_join(guild):
	checkmute(guild)

async def checkmute(guild):
	global hasMsgMute
	global hasTotalMute
	global hasVCMute
	hasMsgMute = False
	hasTotalMute = False
	hasVCMute = False
	class MsgPerms:
		send_messages = False
		send_tts_messages = False
		speak = True
		stream = True
		value = 3146240
	class VCPerms:
		speak = False
		stream = False
		read_messages = True
		send_messages = True
		read_message_history = True
		value = 68608
	class TotalPerms:
		send_messages = False
		speak = False
		stream = False
		read_message_history = False
		value = 0
	roles = await guild.fetch_roles()
	count = 0
	for x in roles:
		if "Message Mute" == x.name:
			global MsgMute
			hasMsgMute = True
			MsgMute = guild.get_role(x.id)
		elif x.name == "Total Mute":
			global TotalMute
			hasTotalMute = True
			TotalMute = guild.get_role(x.id)
		elif x.name == "VC Mute":
			global VCMute
			hasVCMute = True
			VCMute = guild.get_role(x.id)
		else:
			count += 1
			if count == len(roles):
				break
			else:
				continue
	if hasMsgMute == False:
		global MsgMute
		MsgMute = await guild.create_role(name="Message Mute", permissions=MsgPerms, colour=discord.Colour.light_grey(), hoist=False, mentionable=False, reason="For mute command")
	if hasTotalMute == False:
		global TotalMute
		TotalMute = await guild.create_role(name="Total Mute", permissions=TotalPerms, colour=discord.Colour.light_grey(), hoist=False, mentionable=False, reason="For mute command")
	if hasVCMute == False:
		global VCMute
		VCMute = await guild.create_role(name="VC Mute", permissions=VCPerms, colour=discord.Colour.light_grey(), hoist=False, mentionable=False, reason="For mute command")
	positions = {
		MsgMute: 2,
		TotalMute: 1,
		VCMute: 3
	}
	await guild.edit_role_positions(positions=positions)
	db["muteroles-" + guild.id] = True

bot.run(os.getenv("token"))