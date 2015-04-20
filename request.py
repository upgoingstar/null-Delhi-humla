import requests
from bs4 import BeautifulSoup
req = requests.get("http://demo.testfire.net")
html = req.text
soup = BeautifulSoup(html)
#prints title of the page.
print soup.title
#prints HTTP Respone code of the page
print soup.status_code
#print body of the Page. 
print soup.text
