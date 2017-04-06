import urllib.request, codecs, threading, queue, math, sys
#from PyQt5.QtWidgets import QApplication, QWidget
from bs4 import BeautifulSoup

class Parser: 
	#############################################################
	# Configurations

	reqHeader = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0 Cyberfox/45.0.3'
	}

	baseUri = "https://tmbox.net"
	downloadUri = "https://tmbox.net/dl/"
	pageQuery = "?page="

	DOMcontainers = {
		'SongCount': "div.l-left > div:nth-of-type(10)",
		'SongListEntry': "div.sound-box",
			'CoverLink': "div.sound-box__icon", # Not in use
			'SongLink': "div.title > a",
		'NextPageButton': "a[rel=\"next\"]"
	}

	#############################################################
	# HTTP Requests/Parsing
	def parsePage(self, pageUrl):
		print('Parsing page:', pageUrl)
		req = urllib.request.Request(pageUrl, headers=self.reqHeader)

		try:
			reqObj = urllib.request.urlopen(req)
		except urllib.error.HTTPError as e:
			print(e.reason)
			return False
		except urllib.error.URLError as e:
			print(e.reason)
			return False

		htmlDoc = reqObj.read()

		return BeautifulSoup(htmlDoc, 'html.parser')

	# Parses profile/song list page
	def parseSongList(self, pageUrl, pageNumber=False):
		if pageNumber:
			pageUrl = pageUrl + self.pageQuery + str(pageNumber)

		soup = self.parsePage(pageUrl)

		if not soup:
			return False

		return soup

	# Useless
	# From a parsed page, gets the number of listed songs
	def getSongCount(self, soup):
		import re
		num = soup.select_one(self.DOMcontainers['SongCount']).string.strip('\n')
		num = re.findall('\d+', num)

		if len(num):
			return int(num[0])

		return False

	# Useless
	# From a parsed page, gets the number of songs per page
	def getSongsPerPage(self, soup):
		return len(soup.select('div.sound-box'))

	# Used for checking if there's a next page
	def getNextPage(self,soup):
		return soup.select(self.DOMcontainers['NextPageButton'])

	def getSongList(self, soup):
		songList = []

		#for a in soup.find_all('a', {'class': 'sound-box'}):
		for entry in soup.select(self.DOMcontainers['SongListEntry']):
			element = entry.select_one(self.DOMcontainers['SongLink'])
			title = element.string.strip('\n')
			link = element['href']

			print(title, link)

			#songList.append(baseUri + a['href'])

	def parsePlayerPage(self, pageUrl):
		global MainWindow, UiMainWindow
		soup = parsePage(pageUrl)

		if not soup:
			return False

		audioElem = soup.select('h1.title')
		audioTitle = audioElem[0].string
		
		pageUrl = pageUrl.split('/')

		resource = urllib.request.urlopen(downloadPage + pageUrl[-1])
		filename = audioTitle + '.mp3'

		if resource.getcode() != 200:
			print('Unable to acquire resource. Skipping...')
			return False

		print('Downloading:', filename.encode(sys.stdout.encoding, errors='replace'))

		with open(filename, 'wb') as f:
			f.write(resource.read())

	#def startParser(self):
	#	musicPageArray = []

	#	parseMusicList("http://tmbox.net/user/yoiyami_/sound", musicPageArray)

	#	for musicPage in musicPageArray:
	#		parseMusicPage(musicPage)

