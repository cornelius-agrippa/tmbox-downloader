import urllib.request, sys, os.path, re
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from Common import getValidFilename

class Parser: 
	#############################################################
	# Configurations

	reqHeader = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0 Cyberfox/45.0.3'
	}

	URI = {
		'base': "https://tmbox.net",
		'download': "https://tmbox.net/dl/",
		'pageQuery': "?page="
	}

	DOMcontainers = {
		'SongCount': "div.l-left > div:nth-of-type(10)",
		'SongListEntry': "div.sound-box",
			'SongLink': "div.title > a",
			'CoverLink': "div.sound-box__icon > img", # Not in use
		'NextPageButton': "a[rel=\"next\"]"
	}

	DownloadDirectory = "downloaded"
	DefaultExtension = ".mp3"

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
	def parseSongList(self, pageUrl, pageNumber):
		pageUrl = pageUrl + self.URI['pageQuery'] + str(pageNumber)

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

	# Acquires songs published by the user
	def getSongList(self, soup):
		from urllib.parse import urlparse

		songList = []

		for entry in soup.select(self.DOMcontainers['SongListEntry']):
			element = entry.select_one(self.DOMcontainers['SongLink'])

			title = element.string.strip('\n')
			link = element['href']

			element = entry.select_one(self.DOMcontainers['CoverLink'])
			cover = urlparse(element['src'])
			cover = cover.scheme + "://" + cover.netloc + cover.path

			songList.append([title, link, cover])

		return songList

	#
	def downloadSong(self, songEntry):
		if not os.path.exists(self.DownloadDirectory):
			os.makedirs(self.DownloadDirectory)

		fileName = getValidFilename(songEntry[0] + self.DefaultExtension)
		dupe = 1

		# Check for duplicate filename. If found, append a suffix
		while os.path.exists(fileName):
			fileName = getValidFilename(songEntry[0]+ "(" + str(dupe) + ")" + self.DefaultExtension)
			dupe += 1

		songUrn = songEntry[1].split('/')
		songUrl = self.URI['download'] + songUrn[-1]

		print('Downloading\n\tFile:', fileName, "\n\tSource:", songUrl)

		try:
			with urllib.request.urlopen(songUrl) as response, open(os.path.join(self.DownloadDirectory, fileName), 'wb') as out_file:
				data = response.read()
				out_file.write(data)
		except HTTPError as e:
			print('\tERROR: Unable to fetch song. User may have disabled downloads for this song. Error code: ', e.code)
		except URLError as e:
			print('Reason: ', e.reason)
		else:
			print('\tDone')
