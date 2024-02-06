#導入Discord.py
import discord
import json
import requests
import os
from AI import load_tm_model, image_tm

intents = discord.Intents.default() # intents是要求機器人的權限
intents.message_content = True 
client = discord.Client(intents=intents)

model_path = r".\\discord_bot\\keras_model.h5"
class_name_path = r".\\discord_bot\\labels.txt"
model, class_names = load_tm_model(model_path, class_name_path)


with open('.\discord_bot\cogs\setting.json','r',encoding='utf8') as jfile:
	jdata = json.load(jfile)

def download_image(url, filename):
	response = requests.get(url)
	if response.status_code == 200:
		with open(filename, 'wb') as f:
			f.write(response.content)
			print(f"图片已保存为 {filename}")		
	else:
		print("无法下载图片")

def file_image(pred):
	pred = pred.strip()
	pic = discord.File(jdata[pred])
	return pic

@client.event  # 當機器人完成啟動
async def on_ready():
  print(f"目前登入身份 --> {client.user}")
  
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	#排除自己的訊息，避免陷入無限循環
	if message.attachments:
		# 检查附件是否是图片类型
		for attachment in message.attachments:
			if attachment.content_type.startswith('image'):
				print(f"收到圖片: {attachment.url}")
				img_name = f'{message.id}.jpg'
				download_image(attachment.url, img_name)
				prediction, score = image_tm(model, class_names, img_name)
				os.remove(img_name)
				pic = file_image(prediction[2:])
				score = round(score,2)
				score_short = "%.0f%%" % (score * 100)
				await message.channel.send(f'名稱:{prediction[2:]} 準確率:{str(score_short)}', file=pic)
				break
			else:
				print("收到附件，但不是图片。")
				await message.channel.send("請勿投放圖片以外的檔案")
	else:
		if message.content.startswith('輸入:'):	#分割訊息成兩份			
				tmp = message.content.replace(':',' ',1).split(' ',2)
				if len(tmp) == 2:
					predtxt = tmp[1]  # 選取適當的元素
					if predtxt not in jdata:
						print(f'找不到對應的key:{predtxt}')
					else:
						pic= file_image(predtxt)
						await message.channel.send(file=pic)
				elif len(tmp) > 2:
					await message.channel.send("請一次輸入一種")
				else:
					await message.channel.send("無此類項目")
		elif message.content.startswith('請問你認識幾種藥材'):
			msg =  ', '.join([class_name.strip()[2:] for class_name in class_names]) 
			await message.channel.send(f"答: {msg}, 總共{len(class_names)}類。")
		else:
			await message.channel.send("輸入:藥名，或是丟圖片進來")

token = '<token>'
client.run(token)