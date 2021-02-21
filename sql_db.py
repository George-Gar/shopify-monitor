import sqlite3
import requests
import json

##################################~create database~################################################################
conn = sqlite3.connect('kith_products.db')
c = conn.cursor()

# c.execute("""CREATE TABLE kith (
#         name text,
#         price text,
#         size text,
#         in_stock integer,
#         sku text,
#         url text,
#         product_id integer
#         )""" )

##################################~execute database functions~##########################################################
c.execute("SELECT * FROM kith")
print(c.fetchall())

conn.commit()
conn.close()