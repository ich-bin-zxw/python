import re,time
import threading
import httplib2
import os


h=httplib2.Http(cache='.cache',timeout=5)  # timeout is 5 seconds

def geturllist(url):
	url_list=[]
	print(url)        
	response,content=h.request(url)
	p=re.compile(r'.*=(?P<charset>.*)')
	charset=(p.match(response['content-type'])).group('charset')
	html = re.search(r'<ol.*</ol>', content.decode(charset), re.S)
	urls = re.finditer(r'<p><img src="(.+?)jpg" /></p>',html.group(),re.I)
	for i in urls:
		url=i.group(1).strip()+str("jpg")
		url_list.append(url)
	return url_list

def download(down_url):
	name=str(time.time())[:-3]+"_"+re.sub('.+?/','',down_url)
	print(name)
	try:
		response,content = h.request(down_url)
		if(response.status == 200):
			with open("D:\\MM\\"+name,'wb') as fp:
				fp.write(content)	
	except:
		pass


def getpageurl():
	page_list = []
	for page in range(20,22):         # can be any number between 1 to 755,anyway,the second arg shoud larger than the first arg
		url="http://jandan.net/ooxx/page-"+str(page)+"#comments"
		page_list.append(url) 
	return page_list


if __name__ == '__main__':
	try:
		os.mkdir(r"d:\MM")
	except:
		pass

	jobs = []
	pageurl = getpageurl()[::-1]
	for i in pageurl: 
		for (downurl) in geturllist(i):
			jobs.append(threading.Thread(target=download,args=(downurl,)))
		for job in jobs:
			job.start()
		for job in jobs:
			job.join(5)  # set timeout to 5 secondes
		del jobs[:]

