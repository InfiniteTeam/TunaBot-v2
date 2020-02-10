# -*-coding: utf-8-*-

import discord
from discord.ext import tasks, commands
import asyncio
import random
import json
import datetime
import os
import sys
import inspect
from extension import tunabot_embed, tunabot_background, tunabot_webhook, tunabot_utils

# 봇 실행 전에, 데이터를 불러옵니다.

with open('C:/tunabot_token.txt') as token_file: # 토큰 불러옴
    token = token_file.readline()
with open('config.json') as config_file: # 설정 파일 불러옴
    config = json.load(config_file)
with open('balance.json') as balance_file: # 레벨업 조건 파일 불러옴
    balance = json.load(balance_file)
with open('userData.json') as userData_file: # 유저 데이터 파일 불러옴
    userData = json.load(userData_file)

app = commands.Bot(command_prefix="")

prefix = config['prefix'] # 설정 파일에서 명령어 접두사를 가져옵니다.
al = tunabot_utils.aliases
args = tunabot_utils.arguments
color = {'main':0x5b50fa, 'yellow':0xffbb00, 'red':0xf04747, 'green':0x43b581, 'orange':0xf26522}

@app.event
async def on_ready():
    dataLoad.start()
    await app.change_presence(activity=discord.Streaming(name="참치봇V2 | 개발중", url="https://www.twitch.tv/tunabot0"), status=discord.Status.dnd)
    print("Ready: {} : {}".format(app.user.name, app.user.id))
    tunabot_webhook.app_ready()

# 1초 간격으로 데이터 업데이트
@tasks.loop(seconds=1)
async def dataLoad():
    global config
    global userData
    with open('config.json') as config_file:
        config = json.load(config_file)
    with open('balance.json') as balance_file:
        balance = json.load(balance_file)
    with open('userData.json') as userData_file:
        userData = json.load(userData_file)

@app.event
async def on_message(message):
    if message.author.bot or message.author == app.user: # 발신자가 봇이거나 자기 자신인 경우 이벤트 무시
        return

    elif message.channel.type == discord.ChannelType.group or message.channel.type == discord.ChannelType.private: # 채널 타입이 그룹이거나 개인메시지인 경우
        embed = tunabot_embed.embed_text(message, ":warning: **경고**", "개인 메세지로는 참치봇과 대화할 수 없습니다.\n [[ 참치봇 초대하기 ]](https://discordbots.org/bot/536095637368864779)", color['yellow'], message.author)
        await message.channel.send(embed=embed)
        return

    elif message.content.startswith(prefix+"동의"):
        if not str(message.author.id) in userData.keys(): # 메시지 발신자가 유저 목록에 등록되어있지 않은 경우
            embed = tunabot_embed.embed_text(message, "", "", color['main'], message.author)
            embed.add_field(name="아래는 참치봇을 사용하기 위한 약관입니다", value="미숙지의 불이익은 본인에게 있습니다. 또한, Team Wonder. 는 [디스코드 TOS](https://discordapp.com/tos)도 준수합니다.", inline=False)
            embed.add_field(name="사용약관", value="Team Wonder. 의 모든 봇을 사용하는 것은 [원더봇 약관](https://wonderbot.xyz/tos) 에 동의한 것으로 간주됩니다.\n또한 다음약관은 추가됩니다.\n- 봇에서 발생하는 모든 분쟁에 팀은 책임지지 않습니다.", inline=False)
            embed.add_field(name="개인정보취급방침", value="◆ 수집하는 개인정보 항목\n봇의 명령어 이용, 버그 악용방지, 테러 방지 등등을 위해 아래와 같은 개인정보를 수집하고 있습니다.\n수집항목 : 유저 : 닉네임, 아이디, 태그, 접두사로 시작하는 모든 메세지 데이터\n서버 : Discord API 가 제공하는 모든 서버 데이터\n○ 개인정보 수집방법 : 유저 제공, Discord API\n◆ 개인정보의 수집 및 이용목적\n해당 봇은 다음과 같은 목적으로 개인정보를 사용합니다.\n○ 과도한 명령어 도배 방지 및 테러방지\n○ 빠르고 쉽게 서비스 제공\n◆ 개인정보의 보유 및 이용기간\n○ 개인정보는 유저의 파기 요청 전 또는 서비스 종료 전까지 안전하게 보관됩니다.\n◆ 개인정보 제공\n해당 봇은 절대로 제 3자에게 개인정보를 제공하지 않습니다. 하지만 아래의 경우는 예외로 합니다\n○ 제휴 이벤트로 개인정보 제공이 불가피한 경우", inline=False)
            embed.add_field(name="해당 약관들에 동의하셔야 서비스를 이용하실 수 있습니다.", value="동의하시려면 `동의`라고 메세지를 전송해주세요.\n다시 검토하시려면 10초간 기다려주세요.", inline=False)
            await message.channel.send(embed=embed)
            def check_accept(m):
                return m.author == message.author and m.content == "동의"
            try:
                m = await app.wait_for('message', timeout=10.0, check=check_accept)
            except asyncio.TimeoutError:
                embed = tunabot_embed.embed_text(message, ":warning: **경고**", "시간이 초과되었습니다.", color['yellow'], message.author)
                await message.channel.send(embed=embed)
            else:
                today = datetime.date.today()
                userData[str(message.author.id)] = {"money" : 0,"rank" : "","lang" : "kor","level" : 0,"point" : 0,"signDate":today.strftime("%Y-%m-%d"),"membership":"Free"}
                with open('userData.json', 'w') as userData_file:
                    json.dump(userData, userData_file, indent=4, sort_keys=True)
                embed = tunabot_embed.embed_text(message, ":white_check_mark: **동의**", "성공적으로 등록되었습니다.", color['main'], message.author)
                await message.channel.send(embed=embed)
        else:
            embed = tunabot_embed.embed_text(message, ":warning: **경고**", "이미 등록된 계정입니다.", color['yellow'], message.author)
            await message.channel.send(embed=embed)

    elif message.content.startswith(prefix) and not str(message.author.id) in userData.keys():
        embed = tunabot_embed.embed_text(message, ":warning: **경고**", f"아직 등록되지 않았습니다.\n `{prefix}동의` 명령어로 등록할 수 있습니다.", color['yellow'], message.author)
        await message.channel.send(embed=embed)
        return

    elif message.content.startswith(prefix+"핑"):
        ping = int(app.latency*1000)
        if  ping <= 100:
            status = "양호"
            pcolor = color['green']
        elif 100 < ping <= 200:
            status = "보통"
            pcolor = color['yellow']
        elif 200 < ping <= 300:
            status = "나쁨"
            pcolor = color['orange']
        elif 300 < ping:
            status = "매우 나쁨"
            pcolor = color['red']
        embed = tunabot_embed.embed_text(message, f":ping_pong: **{status}**", (f"**봇 지연시간** {str(ping)}ms"), pcolor, message.author)
        await message.channel.send(embed=embed)

    elif message.content.startswith(prefix+"백업"):
        if "Master" in userData[str(message.author.id)]['rank']:
            available = []
            for x in os.listdir():
                if x.endswith(".json"):
                    available.append(x)
            backups = ""
            for y in available:
                backups += y+"\n"
            embed = tunabot_embed.embed_text(message, ":outbox_tray: **백업**", (f"**백업 가능한 파일** - \n{backups}"), color['main'], message.author)
            backup_message = await message.channel.send(embed=embed)
            await backup_message.add_reaction("✅")
            await backup_message.add_reaction("❎")
            def check_backup(reaction, user):
                return user == message.author and str(reaction.emoji) in ["✅","❎"]
            try:
                reaction, user = await app.wait_for('reaction_add', timeout=5.0, check=check_backup)
            except asyncio.TimeoutError:
                embed = tunabot_embed.embed_text(message, ":warning: **경고**", "시간이 초과되었습니다.", color['yellow'], message.author)
                await message.channel.send(embed=embed)
            else:
                if str(reaction.emoji) == "✅":
                    embed = tunabot_embed.embed_text(message, ":outbox_tray: **백업**", (f"**백업 중** - \n{backups}"), color['main'], message.author)
                    await backup_message.edit(embed=embed)
                    now = datetime.datetime.now()
                    #backups = ""
                    for z in available:
                        with open(z, 'rb') as f:
                            dbx.files_upload(f.read(), ("/"+z.replace(".json","")+now.strftime("%Y%m%d%H%M%S")+".json"))
                        backups = backups.replace(z, f"{z} :white_check_mark:")
                        embed = tunabot_embed.embed_text(message, ":outbox_tray: **백업**", (f"**백업 중** - \n{backups}"), color['main'], message.author)
                        await backup_message.edit(embed=embed)
                    embed = tunabot_embed.embed_text(message, ":outbox_tray: **백업**", (f"**백업 완료** - \n{backups}"), color['main'], message.author)
                    await backup_message.edit(embed=embed)

                elif str(reaction.emoji) == "❎":
                    embed = tunabot_embed.embed_text(message, ":outbox_tray: **백업**", "**백업 취소**", color['main'], message.author)
                    await backup_message.edit(embed=embed)
        else:
            embed = tunabot_embed.embed_text(message, ":warning: **경고**", "**Master** 권한이 없습니다.", color['yellow'], message.author)
            await message.channel.send(embed=embed)

    elif message.content.startswith(prefix+"실행"):
        if "Master" in userData[str(message.author.id)]['rank']:
            command = message.content[4:]
            if command == "":
                embed = tunabot_embed.embed_text(message, ":warning: **경고**", "실행 명령어는 **Python** 인수가 필요합니다.", color['yellow'], message.author)
                await message.channel.send(embed=embed)
            else:
                result = exec(command)
                if inspect.isawaitable(result):
                    embed = tunabot_embed.embed_text(message, ":cd: **실행**", await result, color['main'], message.author)
                    await message.channel.send(embed=embed)
                else:
                    embed = tunabot_embed.embed_text(message, ":cd: **실행**", result, color['main'], message.author)
                    await message.channel.send(embed=embed)
        else:
            embed = tunabot_embed.embed_text(message, ":warning: **경고**", "**Master** 권한이 없습니다.", color['yellow'], message.author)
            await message.channel.send(embed=embed)

    elif message.content.startswith(prefix+"프로필"):
        myData = userData[str(message.author.id)]
        percent = myData['point']/balance['l:p'][str(myData['level']+1)]*100
        if myData['rank'] == "":
            rank = "없음"
        else:
            rank = myData['rank']
        embed = tunabot_embed.embed_text(message, ":bust_in_silhouette: **프로필**", "", color['main'], message.author)
        embed.add_field(name=":label: 이름", value=message.author)
        embed.add_field(name=":trophy: 랭크", value=rank)
        embed.add_field(name=":military_medal: 멤버쉽", value=myData['membership'])
        embed.add_field(name="<:wondercoin:653555403606458368> 코인", value=myData['money'])
        embed.add_field(name=":test_tube: 레벨", value=f"Lv.{myData['level']} ({percent}%)")
        embed.add_field(name=":calendar: 서비스 가입일", value=f"{myData['signDate']} (GMT+09:00)")
        embed.set_thumbnail(url=message.author.avatar_url)
        await message.channel.send(embed=embed)

    elif message.content == prefix+"업다운":
        embed = tunabot_embed.embed_text(message, ":arrow_up_down: **업다운 게임**", "", color['main'], message.author)
        embed.add_field(name=":grinning: **쉬움**", value="1에서부터 10까지의 수중 하나로 플레이합니다.")
        embed.add_field(name=":confused: **보통**", value="1에서부터 100까지의 수중 하나로 플레이합니다.")
        embed.add_field(name=":rage: **어려움**", value="1에서부터 1000까지의 수중 하나로 플레이합니다.")
        difficulty = await message.channel.send(embed=embed)
        await difficulty.add_reaction("😀")
        await difficulty.add_reaction("😕")
        await difficulty.add_reaction("😡")
        def check_updown(reaction, user):
            return user == message.author and str(reaction.emoji) in ["😀","😕", "😡"]
        try:
            reaction, user = await app.wait_for('reaction_add', timeout=10.0, check=check_updown)
        except asyncio.TimeoutError:
            embed = tunabot_embed.embed_text(message, ":warning: **경고**", "시간이 초과되었습니다. 게임이 종료됩니다.", color['yellow'], message.author)
            await message.channel.send(embed=embed)
        else:
            if str(reaction.emoji) == "😀":
                tried = 1
                number = random.randint(1,10)
                embed = tunabot_embed.embed_text(message, ":arrow_up_down: **업다운 게임**", "1에서부터 10까지 수중 하나를 입력해주세요.\n시간제한 : **10초**", color['main'], message.author)
                await message.channel.send(embed=embed)
                async def updown(trynum):
                    def check_number(m):
                        return m.channel == message.channel and m.content.isdigit()
                    try:
                        msg = await app.wait_for('message', timeout=10.0, check=check_number)
                    except asyncio.TimeoutError:
                        embed = tunabot_embed.embed_text(message, ":warning: **경고**", "시간이 초과되었습니다. 게임이 종료됩니다.", color['yellow'], message.author)
                        await message.channel.send(embed=embed)
                    else:
                        if int(msg.content) in range(1, 11):
                            if trynum in range(1,11):
                                if int(msg.content) == number:
                                    embed = tunabot_embed.embed_text(message, ":arrow_up_down: **업다운 게임**", f":tada: **정답입니다!** \n시도 횟수 : {trynum}회\n **+{(10-trynum)*10}<:wondercoin:653555403606458368> 획득!**", color['main'], message.author)
                                    await message.channel.send(embed=embed)
                                elif int(msg.content) > number:
                                    embed = tunabot_embed.embed_text(message, ":arrow_up_down: **업다운 게임**", f":arrow_down: **DOWN!** \n**{msg.content}**보다 **작은 수** 입니다.\n다음 수를 입력해주세요.", color['main'], message.author)
                                    await message.channel.send(embed=embed)
                                    await updown(trynum)
                                elif int(msg.content) < number:
                                    embed = tunabot_embed.embed_text(message, ":arrow_up_down: **업다운 게임**", f":arrow_up: **UP!** \n**{msg.content}**보다 **큰 수** 입니다.\n다음 수를 입력해주세요.", color['main'], message.author)
                                    await message.channel.send(embed=embed)
                                    await updown(trynum)
                                await message.channel.send(trynum)
                                trynum += 1
                            else:
                                embed = tunabot_embed.embed_text(message, ":warning: **경고**", "기회가 모두 소진되었습니다. 게임이 종료됩니다.", color['yellow'], message.author)
                                await message.channel.send(embed=embed)
                        else:
                            embed = tunabot_embed.embed_text(message, ":warning: **경고**", "범위 내의 수가 아닙니다. 게임이 종료됩니다.", color['yellow'], message.author)
                            await message.channel.send(embed=embed)
                await updown(tried)

    '''elif message.content.startswith():
        app.load_extension(f"command.{args(message)[0]}")
        embed = tunabot_embed.embed_text(message, ":arrow_up: **로드**", f"**{args(message)[0]}** 기능을 로드했습니다.", color['main'], message.author)
        await message.channel.send(embed=embed)
    
    elif message.content.startswith(prefix+"언로드"):
        app.unload_extension(f"command.{args(message)[0]}")
        embed = tunabot_embed.embed_text(message, ":arrow_up: **언로드**", f"**{args(message)[0]}** 기능을 언로드했습니다.", color['main'], message.author)
        await message.channel.send(embed=embed)

    elif message.content.startswith(prefix+"리로드"):
        app.reload_extension(f"command.{args(message)[0]}")
        embed = tunabot_embed.embed_text(message, ":arrow_up: **리로드**", f"**{args(message)[0]}** 기능을 리로드했습니다.", color['main'], message.author)
        await message.channel.send(embed=embed)'''




            #elif str(reaction.emoji) == "😕":
            #elif str(reaction.emoji) == "😡":'''


app.run(token)