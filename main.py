import asyncio
import os
import requests
import json
import random
import datetime
from datetime import datetime
from datetime import date
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands, tasks
import discord
from discord.commands import Option
from discord.ext.commands import cooldown, BucketType
from discord.ui import Button, View
import dateutil.parser as dp

##API Keys and Disord Token Hidden in .env file
load_dotenv()

token = os.getenv('TOKEN')
KEY = os.getenv('KEY')

intents = discord.Intents.all()
bing = commands.Bot(command_prefix='bc!', intents=intents)

PINK_COLOR = 0xC98FFC

def getInfo(call):
    r = requests.get(call)
    return r.json()

@bing.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f"On cooldown, {round(error.retry_after, 2)} seconds left")

@bing.event
async def on_ready():
  print("██████╗ ██╗███╗   ██╗ ██████╗  ██████╗ ██████╗ ██╗███╗   ██╗")
  print("██╔══██╗██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗██║████╗  ██║")
  print("██████╔╝██║██╔██╗ ██║██║  ███╗██║     ██║   ██║██║██╔██╗ ██║")
  print("██╔══██╗██║██║╚██╗██║██║   ██║██║     ██║   ██║██║██║╚██╗██║")
  print("██████╔╝██║██║ ╚████║╚██████╔╝╚██████╗╚██████╔╝██║██║ ╚████║")
  print("╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝")
  await bing.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Transcripts | bingleton#0001"), status=discord.Status.dnd)

@bing.event
async def on_member_join(member):
    if member.guild.id == 1060377943483879516:
        log = bing.get_channel(1060692849970139267)
        embed = discord.Embed(description=f"{member.mention} {member}", color=0xAFE1AF)
        embed.set_author(icon_url=member.display_avatar, name="Member Joined")
        user = bing.get_user(member.id)
        embed.add_field(name="Account Creation", value=f"<t:{int(user.created_at.timestamp())}:D>")
        embed.set_thumbnail(url=member.display_avatar)
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"ID: {member.id}")
        msg = await log.send(embed=embed)
        welcome_channel = bing.get_channel(1060377944079478846)
        user = bing.get_user(member.id)
        embed = discord.Embed(title="Welcome", description=f"Welcome to **{member.guild}**, {member.mention}!\n\nUsername - {member}\nCreation Date - <t:{int(user.created_at.timestamp())}:D>\nMember #{msg.guild.member_count:,}", color=PINK_COLOR)
        embed.timestamp = datetime.now()
        embed.set_thumbnail(url=member.display_avatar)
        await welcome_channel.send(embed=embed)

@bing.event
async def on_message(message):
    allowedTypeVerify = [1060702854043672676, 931994788864086128]
    if message.author.id in allowedTypeVerify:
        return
    else:
        try:
            await message.author.kick()
            await message.delete()
            embed = discord.Embed(title=f"{message.author} attempted to type in Verify", color=0xFFCE33)
        except:
            embed = discord.Embed(title=f"⚠️ {message.author} could not be kicked", color=0xFF3333)
        channel = bing.get_channel(1060711789970591865)
        await channel.send(embed=embed)

@bing.slash_command()
async def sell(ctx, name:Option(str, "Name of Account", required=True), cost:Option(int, "Cost of Account", required=True), channelid:Option(str, "Channel ID to send Account Information", required=True)):
    try:
        try:
            user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        except:
            embed=discord.Embed(title="Invalid Username", description="Make sure you spelled the username correctly", color=0xAA4A44)
            embed.set_footer(text=f"Command executed by {ctx.author.name} | Powered by itsb1ng.dev")
            await ctx.respond(embed=embed)
            return

        responseMsg = await ctx.respond("Valid Username")
        uuid = user_name["id"]
        sb_data = requests.get(f"https://api.hypixel.net/skyblock/profiles?key={KEY}&uuid={uuid}").json()
        profileData = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{name}").json()
        for i, profileId in enumerate(profileData['profiles']):
            if profileData['profiles'][profileId]['current'] is True:
                profile_id = profileId
                break

        for z in range(0,len(sb_data['profiles'])):
            if sb_data['profiles'][z]['profile_id'] == profile_id:
                profile_num = z

        def number_format(num):
            if num is None:
                format_number = 0
            elif num > 1000000000:
                format = num / 1000000000
                format_number = f"{format:.2f}b"
            elif num > 1000000:
                format = num / 1000000
                format_number = f"{format:.1f}m"
            elif num > 1000:
                format = num / 1000
                format_number = f"{format:.1f}k"
            return format_number
        
        def zero_checker(num):
            if num is None:
                num = 0
                return num

        profile_name = sb_data['profiles'][profile_num]["cute_name"]

        profile = sb_data['profiles'][profile_num]['members'][uuid]

        dict = {"data": profile}

        networth_data = requests.post("https://skyblock.acebot.xyz/api/networth/categories", json=dict).json()
        try:
            AccountTest = networth_data['data']['networth']
        except:
            await responseMsg.edit_original_message(content="All APIs not available")
            return
        try:
            combined = zero_checker(networth_data['data']['bank']) + zero_checker(networth_data['data']['purse'])
        except:
            combined = 0
        networth = number_format(networth_data['data']['networth'] + combined)
        embed = discord.Embed(title=f"{networth} ➜ ${cost}", color=PINK_COLOR)
        embed.set_author(icon_url="https://static.wikia.nocookie.net/hypixel-skyblock/images/f/fb/Personal_Bank.png/revision/latest?cb=20191231173037", name=f"{user_name['name']} on {profile_name}", url=f"https://sky.shiiyu.moe/stats/{user_name['name']}/{profile_name}#")
        embed.add_field(name="Networth", value=networth, inline=False)
        embed.add_field(name="Purse", value=number_format(networth_data['data']['purse']), inline=True)
        embed.add_field(name="Bank", value=number_format(networth_data['data']['bank']), inline=True)
        embed.add_field(name="Combined", value=number_format(combined), inline=True)

        if len(networth_data['data']['categories']['inventory']['top_items']) > 5:
            inventory_num = 5
        else:
            inventory_num = len(networth_data['data']['categories']['inventory']['top_items']) - 1

        if len(networth_data['data']['categories']['talismans']['top_items']) > 5:
            talisman_num = 5
        else:
            talisman_num = len(networth_data['data']['categories']['talismans']['top_items']) - 1

        if len(networth_data['data']['categories']['enderchest']['top_items']) > 5:
            echest_num = 5
        else:
            echest_num = len(networth_data['data']['categories']['enderchest']['top_items']) - 1

        if len(networth_data['data']['categories']['armor']['top_items']) > 5:
            armor_num = 5
        else:
            armor_num = len(networth_data['data']['categories']['armor']['top_items']) - 1

        if len(networth_data['data']['categories']['wardrobe_inventory']['top_items']) > 5:
            wardrobe_num = 5
        else:
            wardrobe_num = len(networth_data['data']['categories']['wardrobe_inventory']['top_items']) - 1

        if len(networth_data['data']['categories']['storage']['top_items']) > 5:
            storage_num = 5
        else:
            storage_num = len(networth_data['data']['categories']['storage']['top_items']) - 1

        if len(networth_data['data']['categories']['pets']['top_items']) > 5:
            pets_num = 5
        else:
            pets_num = len(networth_data['data']['categories']['pets']['top_items']) - 1

        inventory_string = f"{networth_data['data']['categories']['inventory']['top_items'][0]['name']} ➜ {number_format(networth_data['data']['categories']['inventory']['top_items'][0]['price'])}"
        if inventory_num > 0:
            for i in range(1, inventory_num):
                inventory_string += f"\n{networth_data['data']['categories']['inventory']['top_items'][i]['name']} ➜ {number_format(networth_data['data']['categories']['inventory']['top_items'][i]['price'])}"

        talisman_string = f"{networth_data['data']['categories']['talismans']['top_items'][0]['name']} ➜ {number_format(networth_data['data']['categories']['talismans']['top_items'][0]['price'])}"
        if talisman_num > 0:
            for i in range(1, talisman_num):
                talisman_string += f"\n{networth_data['data']['categories']['talismans']['top_items'][i]['name']} ➜ {number_format(networth_data['data']['categories']['talismans']['top_items'][i]['price'])}"

        echest_string = f"{networth_data['data']['categories']['enderchest']['top_items'][0]['name']} ➜ {number_format(networth_data['data']['categories']['enderchest']['top_items'][0]['price'])}"
        if echest_num > 0:
            for i in range(1, echest_num):
                echest_string += f"\n{networth_data['data']['categories']['enderchest']['top_items'][i]['name']} ➜ {number_format(networth_data['data']['categories']['enderchest']['top_items'][i]['price'])}"

        armor_string = f"{networth_data['data']['categories']['armor']['top_items'][0]['name']} ➜ {number_format(networth_data['data']['categories']['armor']['top_items'][0]['price'])}"
        if armor_num > 0:
            for i in range(1, armor_num):
                armor_string += f"\n{networth_data['data']['categories']['armor']['top_items'][i]['name']} ➜ {number_format(networth_data['data']['categories']['armor']['top_items'][i]['price'])}"

        wardrobe_string = f"{networth_data['data']['categories']['wardrobe_inventory']['top_items'][0]['name']} ➜ {number_format(networth_data['data']['categories']['wardrobe_inventory']['top_items'][0]['price'])}"
        if wardrobe_num > 0:
            for i in range(1, wardrobe_num):
                wardrobe_string += f"\n{networth_data['data']['categories']['wardrobe_inventory']['top_items'][i]['name']} ➜ {number_format(networth_data['data']['categories']['wardrobe_inventory']['top_items'][i]['price'])}"

        storage_string = f"{networth_data['data']['categories']['storage']['top_items'][0]['name']} ➜ {number_format(networth_data['data']['categories']['storage']['top_items'][0]['price'])}"
        if storage_num > 0:
            for i in range(1, storage_num):
                storage_string += f"\n{networth_data['data']['categories']['storage']['top_items'][i]['name']} ➜ {number_format(networth_data['data']['categories']['storage']['top_items'][i]['price'])}"

        pets_string = f"{networth_data['data']['categories']['pets']['top_items'][0]['name']} ➜ {number_format(networth_data['data']['categories']['pets']['top_items'][0]['price'])}"
        if pets_num > 0:
            for i in range(1, pets_num):
                pets_string += f"\n{networth_data['data']['categories']['pets']['top_items'][i]['name']} ➜ {number_format(networth_data['data']['categories']['pets']['top_items'][i]['price'])}"

        embed.set_thumbnail(url=f"https://crafatar.com/renders/head/{uuid}")

        if inventory_num >= 0:
            inventory_emoji = bing.get_emoji(1049518172761489411)
            embed.add_field(name=f"{inventory_emoji} Inventory ➜ {number_format(networth_data['data']['categories']['inventory']['total'])}", value=inventory_string, inline=False)

        if talisman_num >= 0:
            talisman_emoji = bing.get_emoji(1060713147650019399)
            embed.add_field(name=f"{talisman_emoji} Talismans ➜ {number_format(networth_data['data']['categories']['talismans']['total'])}", value=talisman_string, inline=False)

        if echest_num >= 0:
            echest_emoji = bing.get_emoji(1060766263342800988)
            embed.add_field(name=f"{echest_emoji} Ender Chest ➜ {number_format(networth_data['data']['categories']['enderchest']['total'])}", value=echest_string, inline=False)

        if armor_num >= 0:
            armor_emoji = bing.get_emoji(1060766280308772915)
            embed.add_field(name=f"{armor_emoji} Armor ➜ {number_format(networth_data['data']['categories']['enderchest']['total'])}", value=armor_string, inline=False)

        if wardrobe_num >= 0:
            wardrobe_emoji = bing.get_emoji(1060766293915082872)
            embed.add_field(name=f"{wardrobe_emoji} Wardrobe ➜ {number_format(networth_data['data']['categories']['wardrobe_inventory']['total'])}", value=wardrobe_string, inline=False)

        if storage_num >= 0:
            storage_emoji = bing.get_emoji(1060766308280565860)
            embed.add_field(name=f"{storage_emoji} Storage ➜ {number_format(networth_data['data']['categories']['storage']['total'])}", value=storage_string, inline=False)
        
        if pets_num >= 0:
            pets_emoji = bing.get_emoji(1060766328283205735)
            embed.add_field(name=f"{pets_emoji} Pets ➜ {number_format(networth_data['data']['categories']['pets']['total'])}", value=pets_string, inline=False)
        
        embed.set_footer(text=f"Command executed by {ctx.author.name} | Powered by itsb1ng.dev")
        try:
            channel = bing.get_channel(int(channelid))
            await channel.send(embed=embed)
        except:
            await responseMsg.edit_original_message(content="Invalid Channel ID")
            return
    except:
        try:
            embed=discord.Embed(title="API Access Error", description=f"`{user_name['name']}`'s inventory API access is disabled on `{profile_name}`\nPlease enable API access.", color=0xAA4A44)
            embed.set_footer(text="Powered by itsb1ng.dev")
            await ctx.respond(embed=embed)
        except:
            embed=discord.Embed(title="Profile Fetch Error", description=f"The player `{user_name['name']}` does not exist.", color=0xAA4A44)
            embed.set_footer(text="Powered by itsb1ng.dev")
            await ctx.respond(embed=embed)

@bing.slash_command()
async def verify(ctx, name:Option(str, "Your IGN", required=True)):
    try:
        user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
        link = f"https://api.slothpixel.me/api/players/{name}"
        data = getInfo(link)
        user_discord = data['links']['DISCORD']
        if user_discord == str(ctx.author):
            guild = ctx.guild
            verified_role = ctx.guild.get_role(1060685858602225685) #Role to give once verified
            member = ctx.author
            channel = bing.get_channel(1060706600010141868)

            overwrite = discord.PermissionOverwrite()
            overwrite.manage_roles = True

            await channel.set_permissions(member, overwrite=overwrite)
            await member.add_roles(verified_role)

            overwrite.manage_roles = False
            await channel.set_permissions(member, overwrite=overwrite)

            namemc = discord.utils.get(bing.emojis, name='namemc')
            skycrypt = discord.utils.get(bing.emojis, name='skycrypt')
            namemc_link = f"https://namemc.com/search?q={user_name['name']}"
            skycrypt_link = f"https://sky.shiiyu.moe/stats/{user_name['name']}/#"
            embed = discord.Embed(title="✅ You're all set", description=f"{ctx.author.mention} verified as `{user_name['name']}`\n{namemc} [NameMC Profile]({namemc_link})\n{skycrypt} [Skycrypt Link]({skycrypt_link})", color=0x68FF33)
            embed.set_thumbnail(url=f"https://crafatar.com/avatars/{user_name['id']}")
            embed.timestamp = datetime.now()
            bingle = bing.get_user(931994788864086128)
            embed.set_footer(text=bingle, icon_url=bingle.display_avatar)
            await ctx.respond(embed=embed)
            
            verificationChannel = bing.get_channel(1060711789970591865)
            embed = discord.Embed(title=f"{user_name['name']}", description=f"{ctx.author.mention} verified as `{user_name['name']}`\n{namemc} [NameMC Profile]({namemc_link})\n{skycrypt} [Skycrypt Link]({skycrypt_link})", color=0x68FF33)
            embed.set_thumbnail(url=f"https://crafatar.com/avatars/{user_name['id']}")
            embed.timestamp = datetime.now()
            member = bing.get_user(ctx.author.id)
            embed.set_thumbnail(url=member.display_avatar)
            await verificationChannel.send(embed=embed)
        
        elif user_discord == None:
            user_name = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}").json()
            await ctx.respond(f"{user_name['name']} does not have a linked Discord")
        
        else:
            await ctx.respond(f"You cannot verify as {user_name['name']}")
        
    except:
        await ctx.respond(f"Unable to verify {name}")

@bing.slash_command()
async def transcript(ctx, player:Option(discord.Member, "Customer", required=True), product:Option(str, "What was purchased?", required=True, choices=["Coins", "Account", "Profile"]), cost:Option(int, "Cost of Product", required=True), notes:Option(str, "Notes for future reference", required=True)):
    file = open('transcript.txt', 'a')
    transactionId = f"{random.randint(999, 9999)}-{random.randint(999, 9999)}-{random.randint(999, 9999)}-{random.randint(999, 9999)}"

    file = open(f"{transactionId}.txt", "w")
    user_messages = await ctx.channel.history(limit=None).flatten()
    user_messages.reverse()
    for item in user_messages:
        try:
            file.write(f"[{item.created_at.strftime('%m/%d/%Y, %H:%M:%S')}] {item.author.name}#{item.author.discriminator}: {item.content}\n")
        except:
            pass
    file.close()

    transactionLog = bing.get_channel(1060722141236035585)
    embed = discord.Embed(title="Transcript Generated", description=f"{player} ● {player.id}", color=PINK_COLOR)
    embed.add_field(name="Transaction ID", value=transactionId, inline=False)
    embed.add_field(name="Seller", value=f"{ctx.author} - {ctx.author.id}", inline=False)
    embed.add_field(name=f"Product", value=product, inline=True)
    embed.add_field(name=f"Cost", value=f"${cost}", inline=True)
    embed.timestamp = datetime.now()
    embed.set_thumbnail(url=player.display_avatar)

    await ctx.respond(embed=embed)

    await transactionLog.send(embed=embed, file=discord.File(f"{transactionId}.txt"))
    os.remove(f"{transactionId}.txt")

    try:
        await player.send(embed=embed)
    except:
        pass
    
    with open(f"transcript.txt", "a") as f:
        f.write(f"Transaction ID: {transactionId}\nCustomer: {player} - {player.id}\nSeller: {ctx.author} - {ctx.author.id}\nCost: ${cost}\nNotes: {notes}\n\n")
        f.close()

bing.run(token)