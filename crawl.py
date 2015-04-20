import requests, sys, re
from bs4 import BeautifulSoup
from urlparse import urlparse

# base_url is the URL to start crawling on.
base_url = 'http://www.humla.com'

# Parse the URL so that we can use it for comparing domain name and checking URL paths
base_parsed = urlparse(base_url)

# Empty list to store all crawled links
links = []

# Session Object to store session information sfter login
s = requests.Session()

# FUNCTION: get_data(url, session_object)
## This function opens a URL using the session_object to maintain login session.
## After opening the URL, passes the HTML content to BeautifulSoup to parse HTML. 
## This function returns parsed HTML from BeautifulSoup if the URL returns a 200, else returns an empty BeautifulSoup object.

def get_data(url, s):
	# Parse the URL for analyzing the different parts
	url_parsed = urlparse(url)
	
	# Check if URL has a Domain Name
	if url_parsed.netloc:

		# If URL has Domain Name, compare and check if its the same domain as base_url,
		# because if a page has http://www.facebook.com link, we don't want to crawl that.
		if base_parsed.netloc.strip() == url_parsed.netloc.strip():

			# Construct the URL with the base_url scheme, url domain name and url path.
			url = "%s://%s/%s" % (base_parsed.scheme.strip(), url_parsed.netloc.strip(), url_parsed.path.strip())

		# url is not the same domain as base_url, so we'll just skip that, so simply return an empty BeautifulSoup object
		else:
			return BeautifulSoup("")

	# url did not have a Domain Name, so it's a relative URL like: login.php or /account.php
	else:
		
		# Construct URL with bae_url scheme, base_url domain name and the path from URL
		url = "%s://%s/%s" % (base_parsed.scheme.strip(), base_parsed.netloc.strip(), url_parsed.path.strip())

	# Open the page with the session_object
	page = s.get(url)

	# We'll pass the page to BeautifulSoup only if it returns a 200 OK. Otherwise return an empty string.
	if page.status_code == 200:

		# page.content returns the HTML content of the requested page
		html_doc = page.content

		# Parse the HTML content using BeautifulSoup
		soup = BeautifulSoup(html_doc)
		return soup
	else:
		return BeautifulSoup("")


# FUNCTION: get_link(url, session_object)
## This function will return the links found in a URL.
## We will parse URL from <a> tag and <form> tag.
## From <a> tag we'll get the 'href' attribute.
## From <form> tag we'll get the 'action' attribute.
## This function returns a list of URLs found in the page.

def get_link(url, s):
	
	# Open the URL using the session_object
	page = s.get(url)
	
	# We'll pass the page to BeautifulSoup only if it returns a 200 OK.
	if page.status_code == 200:
		html_doc = page.content
		soup = BeautifulSoup(html_doc)

		# Initialize an empty list to store the URLs on the page.
		urllinks = []

		# soup.find_all('a') will return a list of all the <a> tags in the page
		for tag in soup.find_all('a'):
			
			# Iterating over each link we'll get the URL from href attribute
			link = tag.get('href')
			link = str(link).strip()
			
			# Since a page can have same URL in multiple locations like Header and Footer,
			# we will not add the URL in the list if already added
			if not link in urllinks:
				urllinks.append(link)
		
		# Same login as above for <form> tag now, the attribute used is action
		for tag in soup.find_all('form'):
			link = tag.get('action')
			link = str(link).strip()
			if not link in urllinks:
				urllinks.append(link)
		return urllinks

	# Otherwise return an empty list.
	else:
		return []



## -------- PROGRAM STARTS EXECUTION FROM HERE ---------- ##

## Step 1: LOGIN TO WEBSITE
print "Attempting Login:",

# Contruct the login URL
login_url = "%s/login.php" % base_url

# post_data dictionary contains the key value pair of the form values submitted with the form. 
post_data = {"login": "cust", "password": "cust", "btnlogin": "Login"}

# We'll use the session object to make the post call since it will store the session information and therefore,
# further requests will use this authenticated session object.
login_response = s.post(login_url, data = post_data)

# To check if successfully logged in, we'll check if a string on the page (after login) exists in the HTML content returned to us
if "My Accounts" in login_response.content:
	print "Login Successful"

# If that string is not present, we'll print out a message and exit from the program 
else:
	print "Login Failed"
	sys.exit(0)
print ""

# Step 2: Once logged in, let's open the base_url to find URLs on that page. We'll get a list of URLs in links
print "Crawled URLs:"
links = get_link(base_url, s)

# Stp 3: Iterate ove each link found on the page (base_url) and then crawl all links in the application
for r in links:
	
	# We will skip the logout URL, since that destroys the session, so we don't want to login again. So just skip it.
	if "logout" in r:
		continue

	# Call the get_data function to return the parsed HTML content from BeautifulSoup. 
	soup = get_data(r, s)

	# try block beacuse when we call find_all below, since we returned an empty BeautifulSoup, 
	# find_all on that empty object will give an exception.
	try:
		
		# This logic is the same as used in get_link function above. Read there for more information.
		for tag in soup.find_all('a'):
			link = tag.get('href')
			link = str(link).strip()
			
			# The important thing to note here is that we are using the same `links` list to append to,
			# since we are iterating over it, if any new link is found that has not already been found 
			# anywhere, we'll add it to the list so that when for loop iteration continues, we'll also 
			# iterate over the new link. This ensures that all links are covered in the application.
			if not link in links:
				links.append(link)
		for tag in soup.find_all('form'):
			link = tag.get('action')
			link = str(link).strip()
			if not link in links:
				links.append(link)

	# If an empty BeautifulSoup object is returned, find_all gives an exception,
	# handling that exception, we'll just skip it using the `pass` statement.
	except:
		pass

# Step 4: One we have all URLs, time to find the exploitable URL

# Initialize an empty String that will hold the exploitable URL from the crawled URLs
exploit_url = ""

# Regex Pattern to search an Email ID in the HTML content
regex = ".+?@.+?\..+?"

# Using the compile function in re library for using regex
pattern = re.compile(regex)

# Reaching here, `links` list will have all links crawled in the website, so we'll just print it out.
for w in links:
	url = "%s://%s/%s" % (base_parsed.scheme.strip(), base_parsed.netloc.strip(), w)
	print url
	response = s.get(url)
	html = response.content

	# search method on pattern will use the regex to search for an email in the HTML content
	if pattern.search(html):
		exploit_url = url

# Step 5: Finally, print out the Exploitable URL
print ""
exploit = "| Expolit URL: %s |" % exploit_url
print "+%s+" % ("-" * (len(exploit) - 2))
print exploit
print "+%s+" % ("-" * (len(exploit) - 2))
