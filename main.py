import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import itertools
import random
import json
authorized_users = [
    "332492309637758977", # owner
    "210593330101354496"  # owner
]
with open("jokes.json") as file:
    jokes = json.load(file)
bot = Bot(command_prefix="y!")
bot.remove_command("help")
status_list = [("with users", 0), ("debugging...", 0), ("Someone code me", 3), ("with my code", 0), ("Coding...", 3), ("the user", 2), ("with commands", 0), ("for user to sdd me", 2)]
async def change_status():
    await bot.wait_until_ready()
    msgs = itertools.cycle(status_list)
    while not bot.is_closed:
        next_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=next.status[0], type=next_status[1]))
        await asyncio.sleep(10)
@bot.event
async def on_ready():
    pass
@bot.event
async def on_member_join(member):
    welcome_embed_description = "Welcome to Our Server, {}!  We hope you enjoy your time here!".format(member.mention)
    embed = discord.Embed(title="New Member", description=welcome_embed_description, color=0x149900)
    embed.set_footer(text="New Member Count: " + str(len(member.server.members)))
    channel = discord.utils.get(member.server.channels, name="welcome-leave")
    await bot.send_message(channel, embed=embed)
    embed = discord.Embed(title="Welcome!", description="Please make sure to verify yourself in the 'verify' channel.", color=0x149900)
    await bot.send_message(member, embed=embed)
@bot.event
async def on_member_remove(member):
    welcome_embed_description = "{} just left. :cry:".format(member.mention)
    embed = discord.Embed(title="Member Left", description=welcome_embed_description, color=0x990000)
    embed.set_footer(text="New Member Count: " + str(len(member.server.members)))
    channel = discord.utils.get(member.server.channels, name="welcome-leave")
    await bot.send_message(channel, embed=embed)
@bot.command(pass_context = True)
async def mute(ctx, member: discord.Member):
    if ctx.message.author.id in authorized_users:
        role = discord.utils.get(member.server.roles, name="Muted")
        await client.add_roles(user, role)
        embed = discord.Embed(title="Mute", description="Successful", color=0x149900)
        embed.add_field(name="User", value=member.id, inline=False)
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="You do not have permission to use that command, {}.".format(ctx.message.author.name), color=0x990000)
        await bot.say(embed=embed)
@bot.command(pass_context = True)
async def unmute(ctx, member: discord.Member):
    if ctx.message.author.id in authorized_users:
        role = discord.utils.get(member.server.roles, name="Muted")
        await client.remove_roles(user, role)
        embed = discord.Embed(title="Unmute", description="Successful", color=0x149900)
        embed.add_field(name="User", value=member.id, inline=False)
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="You do not have permission to use that command, {}.".format(ctx.message.author.name), color=0x990000)
        await bot.say(embed=embed)
@bot.command(pass_context = True)
async def ban(ctx, member: discord.Member, days: int = 1):
    if ctx.message.author.id in authorized_users:
        await bot.ban(member, days)
        embed = discord.Embed(title="Ban", description="Successful", color=0x149900)
        embed.add_field(name="User", value=member.id, inline=False)
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="You do not have permission to use that command, {}.".format(ctx.message.author.name), color=0x990000)
        await bot.say(embed=embed)
@bot.command(pass_context=True)
async def unban(ctx, *, member):
    if ctx.message.author.id in authorized_users:
        server = ctx.message.server
        bans = await bot.get_bans(server)
        try:
            # First we'll try matching with the exact user id
            uid = int(member)
            uid = str(uid)
            matches = list(filter(lambda u: u.id == uid, bans))
            if not matches:
                return await bot.say('no users ids matched with %s' % uid)
            _member = matches[0]
        except ValueError:
            # If the provided string isn't an id we'll try to get an exact match on a user from the bans list
            # The member string needs to be exactly the same as the users name + discrim combo like this Testuser#7777
            matches = list(filter(lambda u: str(u) == member, bans))
            if not matches:
                return await bot.say('no users matched with %s' % member)
            _member = matches[0]
        await bot.unban(ctx.message.server, _member)
        embed = discord.Embed(title="Unban", description="Successful", color=0x149900)
        embed.add_field(name="User", value=member.id, inline=False)
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="You do not have permission to use that command, {}.".format(ctx.message.author.name), color=0x990000)
        await bot.say(embed=embed)
@bot.command(pass_context = True)
async def kick(ctx, member: discord.Member):
    if ctx.message.author.id in authorized_users:
        await bot.kick(member)
        embed = discord.Embed(title="Kick", description="Successful", color=0x149900)
        embed.add_field(name="User", value=member.id, inline=False)
        await bot.say(embed=embed)
    else:
        embed = discord.Embed(title="Error", description="You do not have permission to use that command, {}.".format(ctx.message.author.name), color=0x990000)
        await bot.say(embed=embed)
@bot.command(pass_context=True)
async def ping(ctx):
    """Sends a reply with the bot latency."""
    t = await bot.say('Pong!')
    ms = (t.timestamp-ctx.message.timestamp).total_seconds() * 1000
    await bot.delete_message(t)
    embed = discord.Embed(title="Ping", description="Pong", color=0x149900)
    embed.add_field(name="Latency", value=str(int(ms)) + " ms", inline=False)
    await bot.say(embed=embed)
    print(f'Ping {int(ping)}ms')
@bot.command(pass_context=True)
async def punch(ctx, user: discord.Member):
    """Punches the specified user."""
    embed = discord.Embed(title="Now Punching", description=user.mention, color=0x149900)
    await bot.say(embed=embed)
    embed_2 = discord.Embed(title="You've been punched!", description="By " + ctx.message.author.name, color=0x149900)
    await bot.send_message(user, embed=embed_2)
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True, manage_messages=True)
async def clear(ctx, amount=100):
    """Clear the specified number of messages, default 100 messages."""
    channel = ctx.message.channel
    messages = []
    amount = int(amount) + 1
    async for message in bot.logs_from(channel, limit=amount):
        messages.append(message)
    await bot.delete_messages(messages)
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await bot.send_message(ctx.message.channel, "You do not have permission to use that command.".format(ctx.message.author.mention))
@bot.command(pass_context=True)
async def members(ctx):
    """Return the server member count."""
    embed = discord.Embed(title="Member Count", description=str(len(ctx.message.server.members)), color=0x149900)
    await bot.say(embed=embed)
@bot.command(pass_context=True)
async def joke(ctx):
    """Tell a joke."""
    joke = random.choice(jokes)
    embed = discord.Embed(title="Joke", description=joke["body"], color=0x149900)
    embed.set_footer(text="Joke #: " + str(joke["id"]))
    await bot.say(embed=embed)
@bot.command(pass_context=True)
async def dm(ctx, user: discord.Member, *, msg: str):
    """Sends a DM message to the specified user."""
    if ctx.message.author.id in authorized_users:
        embed = discord.Embed(title="Now sending message", description=msg, color=0x149900)
        embed.set_footer(text=user.name)
        await bot.say(embed=embed)
        embed_2 = discord.Embed(title="You've received a message!", description=msg, color=0x149900)
        embed_2.set_footer(text=ctx.message.author.name)
        await bot.send_message(user, embed=embed_2)
    else:
        embed = discord.Embed(title="Error", description="You do not have permission to use that command, {}.".format(ctx.message.author.name), color=0x990000)
        await bot.say(embed=embed)
    await bot.delete_message(ctx.message)
@bot.command(pass_context=True)
async def suggest(ctx, *, msg: str):
    user_formatted = ctx.message.author.name + "#" + ctx.message.author.discriminator
    channel = discord.utils.get(ctx.message.server.channels, name="suggestions")
    embed = discord.Embed(title="New Suggestion", description=msg, color=0x149900)
    embed.set_author(name=user_formatted, icon_url=ctx.message.author.avatar_url)
    embed_message = await bot.send_message(channel, embed=embed)
    await bot.add_reaction(embed_message, '👍')
    await bot.add_reaction(embed_message, '👎')
    embed_2 = discord.Embed(title="Success", description="Your suggestion has been sent.", color=0x149900)
    await bot.send_message(ctx.message.channel, embed=embed_2)
    await bot.delete_message(ctx.message)
@bot.command(pass_context=True)
async def help(ctx):
    """Show help."""
    embed = discord.Embed(title="Help", description="These are the commands you can use.", color=0x149900)
    embed.add_field(name="y!help", value="Show this message.", inline=False)
    embed.add_field(name="y!ping", value="Send the bot latency.", inline=False)
    embed.add_field(name="y!punch (user)", value="DM punch the user.", inline=False)
    embed.add_field(name="y!clear (limit)", value="Clear the specified number of messages.", inline=False)
    embed.add_field(name="?members", value="Send the server member count.", inline=False)
    embed.add_field(name="y!joke", value="Send a joke.", inline=False)
    embed.add_field(name="y!suggest (suggestion)", value="Sends a suggestion to the server staff.", inline=False)
    embed.add_field(name="y!ban (user)", value="Bans the user.", inline=False)
    embed.add_field(name="y!unban (user)", value="Unbans the user.", inline=False)
    embed.add_field(name="y!kick (user)", value="Kicks the user.", inline=False)
    await bot.say(embed=embed)
bot.loop.create_task(change_status())
bot.run(os.getenv("TOKEN"))
