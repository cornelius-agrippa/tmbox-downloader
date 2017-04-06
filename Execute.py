import TmBoxParser
import sys

#############################################################
# Execution Block
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print ("Missing argument. Usage: python", sys.argv[0], "https://tmbox.net/user/<username>")
		#sys.exit()

	currentPage = 1

	parser = TmBoxParser.Parser()

	while True:
		result = parser.parseSongList("https://tmbox.net/user/yoiyami_", currentPage)

		#numOfSongs = parser.getSongCount(result)

		#if not numOfSongs:
		#	print ("No songs found for provided user.")
		#	break

		parser.getSongList(result)

		if not len(parser.getNextPage(result)):
			print ("Job is done")
			break

		currentPage += 1
