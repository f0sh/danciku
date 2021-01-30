# generate csv wordlist
import re
from cedict_utils.cedict import CedictParser




class DictParser():

	def __init__(self):
		self._dictentries = []
		self._dictlang = ''
		self._wordlist = []

	def downloadDict(self, language):
		# downloads an updates version of the dictionary
		urls = {
				'zh-de': 'https://github.com/gugray/HanDeDict/blob/master/handedict.u8',
				'zh-en': 'https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip'}
		pass

	def downloadFrequency(self):
		pass


	def cleanDict(self):
		# cleans a dictionary and reloads it into the class

		new = []
		for e in self._dictentries:
			e.raw_line = re.sub(r'([\;\/][\s]?Bsp.:[^\;\/]*)(?=[\;\/])', '', e.raw_line) # remove german examples
			# e.raw_line = re.sub(r'\(Bsp.:[^\)]*\)', '', e.raw_line) # remove german short examples
			new.append(e.raw_line)

		# del(parser)
		parser = CedictParser(lines=new)
		self._dictentries = parser.parse()



	def _filterMeaning(self, meaning):
		meaning = re.sub(r'\(Bsp.:[^\)]*\)', '', meaning)
		return meaning

	def saveDict(self):
		# exports a minimized and sanitized cc-CEDICT dictionary to a file

		filename = self._dictlang + '.u8'

		with open(filename, 'w') as file:
			for e in self._dictentries:
				file.write(e.raw_line + "\n")



	def loadDict(self, filename, language):
		# load a cc-CEDICT dictionary with the [cedict-parser](https://github.com/marcanuy/cedict_utils)
		# loads the list of entries into global variable

		parser = CedictParser(file_path=filename)
		self._dictentries = parser.parse()
		self._dictlang = language



	def loadWordlist(self, filename):
		# loads a wordlist, which should contain the word to learn (characters) \t and comments, like unit, etc.
		# example entry: 厦门市	Unit 4

		with open(filename, 'r') as file:

			for l in file:

				line = l.split("\t", 1)
				self._wordlist.append({'char': line[0], 'comment': line[1].rstrip()})


	def extendWordlist(self, filename):

		new = []
		for word in self._wordlist:
			found = False # set a found variable, so that if in case no word can found in the dictionary, the word is not lost in the wordlist
			for entry in self._dictentries:
				if word['char'] == entry.simplified:
					found = True
					
					# combine all meanings
					meaning = ''
					for m in entry.meanings:
						if not meaning:
							meaning += self._filterMeaning(m)
						else:
							meaning += "/ " + self._filterMeaning(m)

					new.append({'simplified': entry.simplified, 'traditional': entry.traditional, 'pinyin': entry.pinyin, 'meaning': meaning, 'comment':word['comment']})

			if not found:
				new.append({'simplified': word['char'], 'comment':word['comment']})

		return new

	def _wordToString(self, word):

		try:
			if word['pinyin']:
				return word['simplified'] + "\t" + word['pinyin'] + "\t" + word['meaning'] + "\t" + word['traditional'] + "\t" + word['comment']
			else:
				return word['simplified'] + "\t" + word['comment']	
		except:
			print(word)
			return word['simplified'] + "\t" + word['comment']	
			


	def exportToCsv(self, filename, export):
		# export a parsed dict and wordlist to a CSV file

		with open(filename, 'w') as file:
			for n in export:
				file.write(self._wordToString(n) + "\n")

# from importlib import reload; reload(DictParser2); dp = DictParser2.DictParser(); dp.loadDict('handedict.u8', 'zh-de');
# import DictParser2; reload(DictParser2); dp = DictParser2.DictParser(); dp.loadDict('dicts/cedict_ts.u8', 'zh-en'); dp.loadWordlist('dc1.txt'); wordlist = dp.extendWordlist(''); 
# 
# export = dp.extendWordlist('wordlist.txt')

