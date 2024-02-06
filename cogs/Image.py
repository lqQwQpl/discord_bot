#導入Discord.py
import discord
import requests
from AI import load_tm_model, image_tm
import json
from discord.ext import commands

class TaskImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        model_path = r".\\discord_bot\\keras_model.h5"
        class_name_path = r".\\discord_bot\\labels.txt"
        model, class_names = load_tm_model(model_path, class_name_path) 
        with open('./cogs/setting.json','r',encoding='utf8') as jfile:
            self.jdata = json.load(jfile)
    def download_image(url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"图片已保存为 {filename}")
        else:
            print("无法下载图片")
    @commands.Cog.listener()
    async def on_message(self , message: discord.Message ):
        if message.author == self.bot.user:
            return 
        #排除自己的訊息，避免陷入無限循環
        if message.attachments:
            attachment = message.attachments[0]
            content = await attachment.read()
            pic1 = discord.File(content)
            await message.channel.send(file = pic1 )  
        if message.content.startswith('藥材'):
            #分割訊息成兩份
            tmp = message.content.split(" ",2)
            #如果分割後串列長度只有1
            if len(tmp) == 1:
                await message.channel.send("何種藥材？請[藥材 藥名]")
            else:
                if tmp[1] == '黃耆':
                    pic2 = discord.File(self.jdata['pic'][1])
                    await message.channel.send(file = pic2)
async def setup(bot):
    await bot.add_cog(TaskImage(bot))

# 定義名為 Main 的 Cog
# class Main(commands.Cog):
#     def __init__(self, bot: commands.Bot):
#         self.bot = bot

#     # 前綴指令
#     @commands.command()
#     async def Hello(self, ctx: commands.Context):
#         await ctx.send("Hello, world!")

#     # 關鍵字觸發
#     @commands.Cog.listener()
#     async def on_message(self, message: discord.Message):
#         if message.author == self.bot.user:
#             return
#         if message.content == "Hello":
#             await message.channel.send("Hello, world!")

# # Cog 載入 Bot 中
# async def setup(bot: commands.Bot):
#     await bot.add_cog(Main(bot))
