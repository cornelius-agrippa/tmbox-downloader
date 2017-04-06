import TmBoxParser
import sys
import urllib.parse as urlparse

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print ("Missing argument. Usage: python", sys.argv[0], "https://tmbox.net/user/<username>")
		sys.exit()

	#parsed = urlparse.urlparse(sys.argv[1])
	#queries = urlparse.parse_qs(parsed.query)

	#if 'page' in queries:
	#	currentPage = queries['page']
	#else:
	#	currentPage = 1

	currentPage = 1

	parser = TmBoxParser.Parser()

	while True:
		result = parser.parseSongList(sys.argv[1], currentPage)
		songList = parser.getSongList(result)

		if not len(songList):
			print ("No songs found in provided page. Terminating job.")
			break

		for songEntry in songList:
			parser.downloadSong(songEntry)

		if not len(parser.getNextPage(result)):
			print ("Job's done")
			break

		currentPage += 1
