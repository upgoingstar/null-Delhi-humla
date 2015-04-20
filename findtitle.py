#This program takes input from user in form of a file, read the targets, find out proper targets, and then finds the title of their page. 

#import Required libraries.
import requests
import sys
from bs4 import BeautifulSoup
from urlparse import urlparse

#create function which excepts one argument, i.e. Target URL/IP
def perform(target):
	urlp = urlparse(target)
	#Check if the URL is proper or not
	if urlp.scheme and urlp.netloc:
		listurl = urlp.scheme + "://" + urlp.netloc	
	else:
		pass
	#use Try / Except for handling any unforeseen exceptions.
	try:
		req = requests.get(target)
		html = req.text
		soup = BeautifulSoup(html)
		print soup.title
	except:
		print 'Please check if url is correct or not'

#take input from user.
f = open(sys.argv[1])
data = f.readlines()
#remove '\n' from every line, as this will otherwise make a improper URL.
for x in data:
	perform(x.strip('\n'))

	
	
	
	
	
	
