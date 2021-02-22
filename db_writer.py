import sqlite3
import requests
import json
import pprint as p

class title_output():
	def __init__(self, link):
		self.r = requests.get(link)
		self.json_key = json.loads(self.r.text)
		self.products = self.json_key.get('products')
		self.conn = sqlite3.connect('kith_products.db')
		self.c = self.conn.cursor()
		#initiate list for skus
		self.sku_list = []

	def titles(self):
		
		for product in self.products:
			for variant in product['variants']:
				# pr.pprint(variant)
				name = product['title']
				url = 'https://kith.com/products/' + product['handle']
				price = variant['price']
				in_stock = variant['available']
				sku = variant['sku']
				size = variant['title']
				product_id = variant['product_id']
				
				#get list of tuples
				self.c.execute("SELECT sku FROM kith")
				sku_db = self.c.fetchall()
				self.c.execute("SELECT in_stock FROM kith WHERE name = ?",(name,))
				name_db = (self.c.fetchall())
				print(name_db)
				#iterate thru list of tuple & grab value inside tuple then append 2 list
				#compare sku to tuples within list
				#this code below can help us check for new arrivals to the site
				for sku_tuple in sku_db:
					if sku_tuple[0] not in self.sku_list:
						self.sku_list.append(sku_tuple[0])
					if sku in self.sku_list:
						# print('yerrrrrr')
						return
				#print(len(self.sku_list))
				

				#test id's against database to find new products to monitor
				#this means a new product was loaded into the site
				if sku not in self.sku_list:
					print(f'{name} {sku} added to database')
					self.c.execute("INSERT INTO kith (name, price, size, in_stock, sku, url, product_id)"
								   " VALUES (? ,?, ?, ?, ?, ?, ?)", (name, price, size, in_stock, sku, url, product_id))
					# p.pprint(self.c.fetchall())
					self.conn.commit()

titles = title_output('https://kith.com/collections/mens-apparel/products.json')
titles2 = title_output('https://kith.com/products.json')
titles.titles()
titles2.titles()
