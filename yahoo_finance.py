import mechanize    #FOR AUTOMATING THE BROWSER
import cookielib	#FOR HANDLING THE COOKIES
from bs4 import BeautifulSoup     #FOR PARSING THE DATA WE GET FROM THE WEBSITE
import getpass

def loginandfinance(email,password):
	url_main = "https://login.yahoo.com/"
	br = mechanize.Browser()   #instance

	#cookiejar
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)

	#browser options	
	br.set_handle_refresh(False)
	br.set_handle_robots(False)

	br.set_debug_redirects(True)
	br.set_debug_responses(True)
	#br.set_debug_http(True)  ---------- for debugging purposes,shows all the header(GET and POST) 


	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	br.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36')]

	sign_in = br.open(url_main)
	br.select_form(nr=0)


	br["username"] = email
	br["passwd"] = password
	br.method ="POST"

	logged_in = br.submit()
	logincheck = logged_in.read()
	soup = BeautifulSoup(logincheck)


	url_finanace='https://in.finance.yahoo.com/'

	br.find_link(url = url_finanace)
	req = br.follow_link(url=url_finanace)

	url_port = "https://in.finance.yahoo.com/portfolio/p_0/view/v1"
	reqs = br.open(url_port)
	con = reqs.get_data()


	ls=[]
	c=0

	sou=BeautifulSoup(con)
	for script in sou(["script","style","input"]):
		script.extract()

	sp = sou.find_all("span",{"class":"wrapper"})
	for i in sp:
		ls.append(i.get_text())
	del ls[0:8]


	lsdet = ["SYMBOL    ","TIME/DATE ","PRICE     ","CHG      ","CHG%     ","DAY'S LOW ","DAY'S HIGH","VOLUME    ","AVG VOLUME","MKT CAP   "]

	c=0
	while c!=len(ls):
		k=0
		for j in range(c,c+10):

			print lsdet[k],"          ",ls[j]
			k = k+1
		print
		c = c+13


	print "TYPE S OR s to SIGN OUT"
	sigout = raw_input()
	if sigout == "s" or sigout=="S":
		signout = sou.find_all("a")
		for i in signout:
			if i.get_text()==" Sign Out":
				url_signout = i.get("href")

		sout = br.open(url_signout)
	else:
		print "WRONG INPUT"



	




while 1:
	try:
		print
		print
		print "WELCOME"
		print "PLEASE, ENTER YOUR EMAIL ADDRESS,  eg abcd@xyz.com"
		email = raw_input()
		print "PLEASE, ENTER YOUR PASSWORD"
		password = getpass.getpass()        #THE PASSWORD THE USER ENTERS IS NOT SHOWN IN THE TERMINAL AND IT IS STORED AS STRING
		loginandfinance(email,password)

		print "DO WANT TO LOGIN TO SOME OTHER ACCOUNT? y/n"
		ans  =raw_input()
		if ans == 'y' or ans == 'Y':
			pass
		else:
			break

	except :
		print "WRONG EMAIL OR PASSWORD"
		print 
		print 




