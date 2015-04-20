import re
text = "<html>abcdeg sjkhs khs john.doe@test.com kljsh dfklhsd</html>"
import requests
r = requests.get("http://www.humla.com/Maketransfer.php")
html = r.content
pattern = re.compile(".+?@.+?\..+?")
if pattern.search(html):
	print "FOUND EMAIL"
else:
	print "yayyyy"
