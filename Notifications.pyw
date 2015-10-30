#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Notifications.py
#  
#  Copyright 2015 Cermo <Cermo@CERMO-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

class ItemValue():
	"""
	Create value object, and draw it using tkinter.
	"""
	column = 0
	row = 0
	
	def CreateTitleBar(self):
		Bar = tk.Label(root, width=50, text=self.name, relief='groove', bg='#AEBED7', fg='#302E29')
		if self.__class__.row != 0:
			self.__class__.row += 2
			self.__class__.column = 0
		Bar.grid(column=self.column, row=self.row, columnspan=4)
		self.__class__.row += 1

	def CreateLabelWidget(self):
		Label = tk.Label(root, width=11, text=self.name, bg='#AEBED7')
		Label.grid(column=self.column, row=self.row)
	
	def CreateTextWidget(self):
		Text = tk.Text(root, width=10, height=1, bg='#AEBED7')
		Text.insert('insert',str(self.value).replace('.',','))
		Text.grid(column=self.column, row=self.row+1)
		self.__class__.column += 1
		if (self.__class__.column % 4) == 0:
			self.__class__.column = 0
			self.__class__.row += 2
		
	def SetValue(self, value):
		self.value = value
		self.value = float("{0:.4f}".format(float(self.value)))
		
	def __init__(self, name):
		self.name = name
	
	
import Tkinter as tk	
root = tk.Tk()
root.resizable(0,0)
root.configure(background='#AEBED7')
root.title('Notowania')
root.iconbitmap('Gold Bars-50.ico')

# Create dictionay with with keys that should be fetched from internet.
# dictionay[key] = search_pattern, start, stop point to display, and divisor
# Used by threading to fetch values from internet
prices = {}
prices['usdpln'] = ['aq_usdpln_c5']
prices['eurpln'] = ['aq_eurpln_c5']
prices['gbppln'] = ['aq_gbppln_c5']
prices['chfpln'] = ['aq_chfpln_c5']
prices['gc.f'] = ['aq_gc.f_c2', 11, 18]
prices['si.f'] = ['aq_si.f_c3', 11, 18, 100]

# Method used by threading to fetch values from internet
import urllib
def CheckValue(dictionary, key):
	pattern = dictionary.get(key)[0]
	try:
		start = dictionary.get(key)[1]
	except:
		start = 13
	try:
		stop = dictionary.get(key)[2]
	except:
		stop = 20
	try:
		divide = dictionary.get(key)[3]
	except:
		divide = None
	value = urllib.urlopen('http://stooq.pl/q/?s='+key).read()
	value = value[value.find(pattern)+start:value.find(pattern)+stop].replace('.','.')
	if divide != None:
			value = float(value)/divide
	dictionary[key] = float(value)

# Theading use function CheckValue and prices dictionary
import threading
threads = [threading.Thread(target=CheckValue, args=(prices, key)) for key in prices.keys()]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

# List of items that have to be drawed by tkinter
items = []
items.append(['Bar', 'CurrencyBar', 'Currency'])
items.append(['Calc', 'usdpln', 'USD [PLN]', prices['usdpln']])
items.append(['Calc', 'eurpln', 'EURO [PLN]', prices['eurpln']])
items.append(['Calc', 'gbppln', 'GBP [PLN]', prices['gbppln']])
items.append(['Calc', 'chfpln', 'CHF [PLN]', prices['chfpln']])
items.append(['Bar', 'MetallsBar', 'Metalls'])
items.append(['Calc', 'goldusd', 'Gold [USD/oz]', prices['gc.f']])
items.append(['Calc', 'goldgusd', 'Gold [USD/g]', (prices['gc.f']/31.1)])
items.append(['Calc', 'goldpln', 'Gold [PLN/oz]', prices['usdpln'] * prices['gc.f']])
items.append(['Calc', 'goldgpln', 'Gold [PLN/g]', (prices['usdpln'] * prices['gc.f']/31.1)])
items.append(['Calc', 'silverusd', 'Silver [USD/oz]', prices['si.f']])
items.append(['Calc', 'silvergusd', 'Silver [USD/g]', (prices['si.f']/31.1)])
items.append(['Calc', 'silverpln', 'Silver [PLN/oz]', prices['usdpln'] * prices['si.f']])
items.append(['Calc', 'silvergpln', 'Silver [PLN/g]', (prices['usdpln'] * prices['si.f']/31.1)])
items.append(['Bar', 'EmpytBar', ''])

# Create objects for each element from items. Create tkiner obejcts.
for item in items:
	item[1] = ItemValue(item[2])
	if item[0] == 'Bar':
		item[1].CreateTitleBar()
	if item[0] == 'Calc':
		item[1].SetValue(*item[3:])
		item[1].CreateLabelWidget()
		item[1].CreateTextWidget()

root.mainloop()
