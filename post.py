import requests
url = "http://www.humla.com/login.php"
post_data = {"login": "cust", "password": "cust", "btnlogin": "Login"}
s = requests.Session()
response = s.post(url, data = post_data)

print "My Accounts" in response.content

response = s.get(url)

print "My Accounts" in response.content

