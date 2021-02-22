import requests
import json
import Product_Names as p
from discord_webhook import DiscordWebhook as dw
from discord_webhook import DiscordEmbed as de
import aiohttp
import asyncio
import sqlite3
import pprint as pr

class kith():

	def __init__(self, link):

		self.link = link
		self.products = ''
		self.webhook = 'https://discord.com/api/webhooks/774780175841755178/usLjqKHxzAtd6QleitBDPAkAD1KJBG32u9BToZrCtSh6E5veURK-v_ObMcMzAP_888ho'
		self.ghost_webhook = 'https://discord.com/api/webhooks/811639019867865098/5Xlg1o432_bglBxydDtFznMUrJcdtV8Ycx3DAGNM6zjJ0wIapOq77bC2vvNUJyQKX2QL'
		self.early_link_webhook = 'https://discord.com/api/webhooks/810328502838624267/1jrf058mAMcxXUYm9aJhRWsmq_rqwuqrPNAYw0nH1IhvG3vjLVxZjpWGDxIA4TSIvjt0'
		self.logo = 'https://cdn.discordapp.com/attachments/773974917170593802/809939354256146432/image0.png'
		#self.product_names filters our monitor search
		self.product_names = p.product_names
		#self.checked limits whether we post to the webhook based on if we checked for the item already
		self.checked = []
		#database connection
		self.conn = sqlite3.connect('kith_products.db')
		self.c = self.conn.cursor()
		self.sku_list = []
		#product variants
		self.name = ''
		self.url = ''				
		self.price = ''
		self.in_stock = ''
		self.sku = ''
		self.product_id = ''
		self.size = ''
		self.img = ''
		#stock list
		#must append in stock to this list because if the last item of the variant is false it won't
		#post the in stock items of that variant to the webhook
		self.availability = []
		############################# DEFINE PRODUCTS #####################################


	async def product_keys(self, product_index_key):
		#when calling this function pass self.products + the list index & key as an argument
		#this function is for displaying the keys and values in the products dictionary
		for item in product_index_key:
			print(item)
			print('\n')

	
	async def product_url(self, product_key):
		#pass self.products + key
		#define url
		url = 'https://kith.com/products/' + product_key
		return url

	
	async def post_webhook(self, title, url, price, stock, size, img):
		#create webhook
		lab_hook = dw(url=self.webhook)
		ghost_hook = dw(url=self.ghost_webhook)
		#create embed
		embed = de(title='Kith.com', description=f"[{title}]({url})")
		embed.set_thumbnail(url=img)
		embed.add_embed_field(name='Price\n', value=f'{price}\n', inline=False)
		embed.add_embed_field(name='In-Stock\n', value=f'{stock}\n', inline=False)
		embed.add_embed_field(name='Sizes\n', value=size, inline=False)
		embed.add_embed_field(name='Links\n', value=f'[ATC]({url})\n', inline=False)
		embed.set_footer(icon_url=self.logo, text="LabMonitor | Formula-X LLC")
				

		#add embed to webhooks
		lab_hook.add_embed(embed)
		ghost_hook.add_embed(embed)

		#excute
		lab_hook.execute()
		ghost_hook.execute()

	
	async def availability_check(self):
		async with aiohttp.ClientSession() as session:
			response = await session.get(self.link)
			products = await response.text()
			products = json.loads(products)
			self.products = products['products']
			pr.pprint(products)

		#loop through products in json file
		for product in self.products:

			#get the image for the embed
			for image in product['images']:
				self.img = image['src']
				break

			#MAKE SIZES ONE STRING IN EMBED & GET ALL THE OTHER EMBED ATTRIBUTES
			# loop through variants of each product
			sizes = ''
			for variant in product['variants']:
				self.name = product['title']
				self.url = await self.product_url(product['handle'])				
				self.price = variant['price']
				self.in_stock = variant['available']
				self.sku = variant['sku']
				self.product_id = variant['product_id']
				#only add the in stock sizes below
				if self.in_stock == True:
					self.size = variant['title']
					sizes += f'{self.size} - '
				self.availability.append(self.in_stock)

			for variant in product['variants']:
				
				self.c.execute("SELECT in_stock FROM kith WHERE name = ?", (self.name,))
				db_stock = self.c.fetchall()
				self.c.execute("SELECT sku FROM kith WHERE name = ?", (self.name,))
				db_sku = self.c.fetchall()

				for s in db_sku:
					if s[0] == self.sku:
						for stock in db_stock:
							if stock[0] == 0 and self.in_stock == True:
								self.size = variant['title']
								await self.post_webhook(self.name, self.url, self.price, self.in_stock, self.size, self.img)

				
			# #CHECK FOR IN STOCK ITEMS
			# #loop through variants of each product
			# for variant in product['variants']:
			# 	# self.in_stock = variant['available']
			# 	#check to see if at least one variant in in stock so that we can post it
			# 	#then reset self.availability so it doesn't spam
			# 	if True in self.availability and self.name not in self.checked:
			# 		self.availability = []
			# 		self.in_stock = True
			# 		for title in self.product_names:
			# 			if title in self.name:
							
			# 				await self.post_webhook(self.name, self.url, self.price, self.in_stock, sizes, self.img)
			# 				self.checked.append(product['title'])
			# 				await asyncio.sleep(1)
							




	



footwear = kith('https://kith.com/products.json')
mens_apparel = kith('https://kith.com/collections/mens-apparel/products.json')


