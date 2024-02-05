import discord
import requests
import json
import random
import os
arr=["https://tenor.com/view/travolta-dark-souls-lost-elden-gif-25073066","https://tenor.com/view/dark-souls-ya-sobaka-ti-sobaka-yasosy-biby-gif-19664947","https://tenor.com/view/ranni-waifu-huggable-gif-25937944"]

from discord.ext import commands
from discord.ext.commands import has_permissions,MissingPermissions
from discord import FFmpegPCMAudio

queues={}
def check_queue(ctx,id):
    if queues[id]!=[]:
        voice=ctx.guild.voice_client
        source=queues[id].pop(0)
        player=voice.play(source)

intents=discord.Intents.all()
intents.members=True

client = commands.Bot(command_prefix = '!',intents=intents)
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,activity=discord.Game('With Your Life'))
    print('woooo')
    print('--------------------')
@client.command()
async def ult(ctx):
    await ctx.send('Nihil !!!!! Nihil !!!!! Nihillll!!!!!!!!!!!')

@client.event
async def on_member_join(member: discord.Member):
    channel=client.get_channel(1201937991694811218)
    meme=random.randint(0,2)
    await channel.send(str(arr[meme]))   
    message="welcome to the server!"
    embed=discord.Embed(title=message)
    await channel.send(embed=embed)
    await channel.send(f"{member.mention}")
    url = "https://daddyjokes.p.rapidapi.com/random"

    headers = {
	"X-RapidAPI-Key": "API-KEY",
	"X-RapidAPI-Host": "daddyjokes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    await channel.send(json.loads(response.text)['joke'])

@client.event
async def on_member_remove(member: discord.Member):
    
    channel=client.get_channel(1201937991694811218)
    await channel.send("https://tenor.com/view/git-gitgoodscrub-scrub-noob-getgood-gif-21752358")
    message="git good!!!"
    embed=discord.Embed(title=message,color=0x801875)
    await channel.send(embed=embed)
    await channel.send(f"{member.mention}")

@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel= ctx.message.author.voice.channel
        voice=await channel.connect()
    else:
        await ctx.send("join a voice channel first")

@client.command(pass_context = True)
async def play(ctx,arg="chipi-chipi"):
    try:
        if(ctx.author.voice):
            channel= ctx.message.author.voice.channel
            if ctx.voice_client and ctx.voice_client.channel==channel:
                voice=ctx.guild.voice_client
                source=FFmpegPCMAudio(str(arg).lower()+'.mp3')
                player=voice.play(source,after=lambda x=None: check_queue(ctx,ctx.message.guild.id))
            else:
                await ctx.send("i need to join a voice channel first, please use join command first")
        else:
            await ctx.send("join a voice channel first")
    except:
        await ctx.send("learn spelling")



@client.command(pass_context = True)
async def resume(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused() :
        voice.resume()
    else:
        await ctx.send("currently playing ")

@client.command(pass_context = True)
async def stop(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()

@client.command(pass_context = True)
async def queue(ctx,arg):
    voice=ctx.guild.voice_client
    song=str(arg).lower()+'.mp3'
    source=FFmpegPCMAudio(song)

    guild_id=ctx.message.guild.id
    if guild_id in queues:
        queues[guild_id].append(source)
    else:
        queues[guild_id]=[source]
    await ctx.send("added to queues")

@client.command(pass_context = True)
async def pause(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing() :
        voice.pause()
    else:
        await ctx.send("currently paused ")

    

@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I'm going to buy milk")
    else:
        await ctx.send("I'm not in a channel")

@client.event
async def on_message(message):
    await client.process_commands(message)
    msg=str.lower(message.content)
    if 'shit' in msg:
        await message.delete()
        await message.channel.send("I know where you live")
        
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member: discord.Member,*,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been hospitalised')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,member: discord.Member,*,reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has died')

@kick.error
async def kick_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("you are unpriviliged")

@ban.error
async def ban_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("you are unpriviliged")

@client.command()
async def message(ctx, user:discord.Member,*,message=None):
    await user.send('https://tenor.com/view/dark-souls-ya-sobaka-ti-sobaka-yasosy-biby-gif-19664947')
    message="welcome to the server!"
    embed=discord.Embed(title=message)
    await user.send(embed=embed)



@client.command()
@commands.has_permissions(manage_roles=True)
async def addRole(ctx,user: discord.Member,*,role:discord.Role):
    if role in user.roles:
        await ctx.send(f"{user.mention} already has the role")
    else:
        await user.add_roles(role)
        await ctx.send(f"{role} is added to {user.mention}")

@client.command()
@commands.has_permissions(manage_roles=True)
async def removeRole(ctx,user: discord.Member,*,role:discord.Role):
    if role in user.roles:
        await user.remove_roles(role)
        await ctx.send(f"removed {role} from {user.mention}")
    else:
        
        await ctx.send(f"{role} is not given to {user.mention}")

@addRole.error
async def role_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You dont have permission to run the command")

@addRole.error
async def removeRole_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You dont have permission to run the command")

client.run('BOT-TOKEN')

