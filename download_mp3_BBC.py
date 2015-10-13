"""
Purpose of this program is to download mp3 files from BBC site.
Program can be run in two modes:
- arch mode - download mp3 from archive bbc site
- normal mode - download mp3 from normal bbc site
Default mode is normal mode. Run this script with "arch" paramter to download mp3 from arch site.
"""
import urllib2
import re
import os.path
from sys import argv

bbcMainPage = "http://www.bbc.co.uk/learningenglish/english/features/6-minute-english"
searchedPattern = "/learningenglish/english/features/6-minute-english/ep-\d{6,8}"

bbcMainPageArch = "http://www.bbc.co.uk/worldservice/learningenglish/general/sixminute/"
searchedPatternArch = "/worldservice/learningenglish/general/sixminute/.{,50}.shtml"


def createLinkList(mainPage, searchedPattern):
	page = urllib2.urlopen(mainPage)
	pageContent = page.read()

	links = re.findall(searchedPattern, pageContent)
	mp3toDownload = []

	for i in links:
		subPage = urllib2.urlopen("http://www.bbc.co.uk"+i)
		subPageContent = subPage.read()
		mp3toDownload += re.findall(r'http.{,150}\.mp3', subPageContent)

	mp3toDownload = list(set(mp3toDownload))
	return mp3toDownload


def downloadMp3(mp3toDownload):
	files_downloaded = ""
	files_downloaded_counter = 0
	for line in mp3toDownload:
		mp3file = urllib2.urlopen(line)
		if not os.path.isfile(line[line.rfind("/")+1:]):
			files_downloaded += line[line.rfind("/")+1:] + "\n"
			files_downloaded_counter += 1
			output = open(line[line.rfind("/")+1:],'wb')
			output.write(mp3file.read())
			output.close()
	return files_downloaded, files_downloaded_counter


Mode = ""
try:
	Mode = argv[1]
except:
	pass


if Mode == "arch":
	print "Running in arch mode"
	mp3toDownload = createLinkList(bbcMainPageArch, searchedPatternArch)
else:
	print "Running in normal mode"
	mp3toDownload = createLinkList(bbcMainPage, searchedPattern)


files_downloaded, files_downloaded_counter = downloadMp3(mp3toDownload)
print "-" * 80
print "Downloaded %d new files" % files_downloaded_counter
print "-" * 80
print files_downloaded
print "-" * 80
