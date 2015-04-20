import sys
def url_join(url1, url2):
	return "%s%s" % (url1.split("//")[1], url2.split("//")[1])

try:
	print url_join(sys.argv[1], sys.argv[2])
except:
	print url_join("http://google.com", "http://gmail.com")
