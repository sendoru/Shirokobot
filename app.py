import random
import os
import asyncio
import time
import datetime
from nextcord.ext import commands
from nextcord.utils import get
import nextcord
import nextcord.interactions
import json

from flask import Flask
import requests
app = Flask(__name__)

from threading import Thread

import nextcord
intents = nextcord.Intents.default()
intents.message_content = True

GUILD_IDS = [681739906913009731, 557938492592750634]

with open('constatns.txt', 'r') as f:
    constants = dict()
    while True:
        line = f.readline()
        if not line:
            break
        line = line.split('=')
        constants[line[0]] = line[1]
    TOKEN = constants['TOKEN'].rstrip('\n')
    OWNER_USER_ID = int(constants['OWNER_USER_ID'])
    BACKEND_HOST = constants['BACKEND_HOST'].rstrip('\n')
    BACKEND_PORT = int(constants['BACKEND_PORT'])


with open('food.txt', 'r', encoding='UTF-8') as f:
    content = f.read().split(',')

class Base(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.on_message_callback = []
        
    def more_cog(self, cog):
        if "on_message" in dir(cog):
            self.on_message_callback.append(cog.on_message)
        self.bot.add_cog(cog)

    @commands.Cog.listener()
    async def on_message(self, message):
        for callback in self.on_message_callback:
            await callback(message)
            
class Basics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.llast_msg = {}
        self.last_msg = {}
        
    @commands.Cog.listener()
    async def copypasta(self, message):
    # gonna do something with https://pypi.org/project/python-sql/ later
        repl = False
        cid = message.channel.id
        if (cid in self.last_msg and self.last_msg[cid].content == message.content and
            not (cid in self.llast_msg and self.llast_msg[cid].content == message.content) and
            not self.last_msg[cid].author.id == message.author.id and
            not self.last_msg[cid].author.bot):
            repl = True
        
        if cid in self.last_msg:
            self.llast_msg[cid] = self.last_msg[cid]
        self.last_msg[cid] = message
        
        if repl and len(message.content) > 0:
            await message.channel.send(message.content)
            
    async def on_message(self, message: nextcord.Message):
        await self.copypasta(message)
        guild = message.guild

        if message.author.bot:
            return

        if self.bot.user.mentioned_in(message):
            if not ("@here" in message.content or "@everyone" in message.content):
                await message.reply("안녕. {} 선생님.".format(message.author.mention))
                
        if (is_modding(message.content)):
            # and guild.id != 730408433043505243): // disabled a while
            await message.reply(osu_link(message.content), mention_author = False)
            
        if '흰둥이' in message.content or '흰둥아' in message.content:
            result = random.randint(0, 1)
            reaction_list = ['<:shiroko_stare:1139804463230627871>', '<:koharu_embarrassed:1139807287305846894>']
            await message.add_reaction(reaction_list[result])
            def check(reaction, user):
                return str(reaction) in reaction_list and user == message.author and reaction.message.id == message.id
            try:
                reaction, _user = await self.bot.wait_for("reaction_add", check = check, timeout = 10.0)
            except asyncio.TimeoutError:
                return
            else:
                if reaction_list[result] == str(reaction):
                    await message.reply('선생님. 시킬 거라도 있어?')
    
    @commands.Cog.listener('on_raw_reaction_add')        
    async def add_role(self, payload):
        reaction_list = ['\U00000034\U0000FE0F\U000020E3', '\U00000037\U0000FE0F\U000020E3']
        role_list = ["4K", "7K"]
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = message.guild
        if guild is not None:
            author = await guild.fetch_member(payload.user_id)
            if (channel.id == 730424725678850099 and
                message.id == 929663235886563388 and
                payload.emoji.name in reaction_list):
                role = get(guild.roles, name = role_list[reaction_list.index(payload.emoji.name)])
                await author.add_roles(role)
    
    @commands.Cog.listener('on_raw_reaction_remove')        
    async def remove_role(self, payload):
        reaction_list = ['\U00000034\U0000FE0F\U000020E3', '\U00000037\U0000FE0F\U000020E3']
        role_list = ["4K", "7K"]
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        guild = message.guild
        author = await guild.fetch_member(payload.user_id)
        if (channel.id == 730424725678850099 and
            message.id == 929663235886563388 and
            payload.emoji.name in reaction_list):
            role = get(guild.roles, name = role_list[reaction_list.index(payload.emoji.name)])
            await author.remove_roles(role)

def is_modding(msg):
    if 2 <= msg.count(':'):
        a = msg.find(':')
        b = msg[a + 1:].find(':')
        chk = msg[a + 1:a + 3] + msg[a + 4:a + 7]
        if a == b and chk.isnumeric():
            return True
    return False
    
def osu_link(msg):
    box = []
    box = msg.split()
    new_box = []
    result = ''
    for pos, char in enumerate(box):
        if is_modding(char): 
            new_box.append(char)
        elif pos != 0:
            if is_modding(box[pos - 1]) and char != '-':
                tmp = new_box.pop()
                new_box.append(tmp + '-' + char)
                
    for pos, char in enumerate(new_box):
        new_box[pos] = '<osu://edit/' + char + '>'
        
    if len(new_box) > 1:
        result = '\n'.join(new_box)
    else:
        result = new_box[0]
    return result

class ShirokoBot(commands.Bot):
    def __init__(self, **args):
        super(ShirokoBot, self).__init__(**args)

    @commands.Cog.listener()
    async def on_ready(self):
        user = await self.fetch_user(OWNER_USER_ID)
        await user.send(f"안녕. {user.mention} 선생님")

def main():
    def get_prefix(bot, message):
        prefixes = ['!']
        return commands.when_mentioned_or(*prefixes)(bot, message)
    intents = nextcord.Intents.default()
    intents.dm_messages = True
    intents.message_content = True
    bot = ShirokoBot(command_prefix=get_prefix, description='흰둥이', case_insensitive=True, intents=intents)

    # @bot.event
    # async def on_ready():
    #     user = await bot.fetch_user(OWNER_USER_ID)
    #     await user.send("안녕. {} 선생님. ".format(user.mention))

    base_cog = Base(bot)
    bot.add_cog(base_cog)
    base_cog.more_cog(Basics(bot))

    @bot.slash_command(name="choose", guild_ids=GUILD_IDS, description="입력된 항목 중에 하나를 랜덤하게 고릅니다. 각 항목은 띄어쓰기로 구분됩니다.")
    async def choose(interaction: nextcord.Interaction, args: str):
        args = args.split(' ')
        result = random.randint(0, len(args) - 1)
        # print(args)
        arg_string = ' '.join(args)
        await interaction.send(f"{args[result]} (`{arg_string}` 중에서)")

    @bot.slash_command(name="menu", guild_ids=GUILD_IDS, description="저메추")
    async def wutfood(interaction: nextcord.Interaction):
        result = random.randint(0, len(content) - 1)
        lotto = random.randint(1, 727)
        if 727 == lotto:
            await interaction.send('음... 와타시. >//< {}'.format(interaction.user.mention))
            return
        
        await interaction.send('음... ' + content[result] +'.')

    @bot.slash_command(name="gacha", guild_ids=GUILD_IDS, description="10연차를 돌립니다")
    async def gacha_10(interaction: nextcord.Interaction):
        await interaction.response.defer()
        try:
            res = await requests.get(f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/gacha/", params={'gacha_type': 10})
        except:
            res = None

        if res is None:
            await interaction.followup.send(f'선새니 아로나가 일하기 싫은가봐 (Response Code: None)')
            return

        res.encoding = 'utf-8'

        res = res.text
        res = json.loads(res, )
        message = ""
        for i in res:
            cur_str = f"{i['stars']}☆ {i['name'][i['name'].find(' ') + 1:]}"
            if i['stars'] == 3:
                message += "**" + cur_str + "**" + "\n"
            else:
                message += cur_str + "\n"

        await interaction.followup.send(message)

    bot.run(TOKEN)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def run():
    app.run(host='localhost', port=8080)

def web():
    thread = Thread(target=run)
    thread.start()

if __name__ == "__main__":
    web()
    main()
