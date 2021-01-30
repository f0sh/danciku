# generate csv wordlist
import re
from cedict_utils.cedict import CedictParser




class DictParser():

	def __init__(self):
		self._dict = []
		self._wordlist = []


	def loadDict(self, filename):
		# load a cc-CEDICT dictionary with the cedict parser
		# and harmonize the output

		parser = CedictParser(file_path=filename)
		entries = parser.parse()

		self._dict = list()

		for e in entries:
			parsed = {}

			parsed['traditional'] = e.traditional
			parsed['simplified'] = e.simplified
			parsed['pinyin'] = e.pinyin
			parsed['meaning'] = ''

			m = e.meanings[0]

			# for m in e.meanings:

			# check, if already is meaning in there, if so add /
			if parsed['meaning'] != '':
				parsed['meaning'] += " / "

			# do not add examples to the meanings
			# meaning = re.sub(r'([\;\/][\s]?Bsp.:[^\;\/]*)(?=[\;\/])', '', m) # for full file
			meaning = re.sub(r'([\;\/][\s]?Bsp.:[^\;\/]*)', '', m)
			meaning = re.sub(r'\(Bsp.:[^\)]*\)', '', meaning)
			parsed['meaning'] += meaning
	
					
			self._dict.append(parsed)


		#with open(filename) as file:
		#	dict_lines = file.read().splitlines()

		#for line in dict_lines:
		#	self._dict.append(self._parse_cedict_line(line))

		#self._remove_surnames(self._dict)
		# self._remove_samples(self._dict)



	def loadWordlist(self, filename):
		with open(filename) as file:
			wordlist_lines = file.read().splitlines()



	def _parse_cedict_line(self, line):
		# parse a single cedict line
		# based on https://github.com/rubber-duck-dragon/rubber-duck-dragon.github.io/blob/master/cc-cedict_parser/parser.py
		
		parsed = {}
		if line == '':
			dict_lines.remove(line)
			return 0
		line = line.rstrip('/')
		line = line.split('/')
		if len(line) <= 1:
			return 0
		english = line[1]
		char_and_pinyin = line[0].split('[')
		characters = char_and_pinyin[0]
		characters = characters.split()
		traditional = characters[0]
		simplified = characters[1]
		pinyin = char_and_pinyin[1]
		pinyin = pinyin.rstrip()
		pinyin = pinyin.rstrip("]")
		parsed['traditional'] = traditional
		parsed['simplified'] = simplified
		parsed['pinyin'] = pinyin
		parsed['english'] = english
		return parsed


	def _remove_surnames(self, list_of_dicts):
		# takes a dictionary and removes all characters for family names
		# based on https://github.com/rubber-duck-dragon/rubber-duck-dragon.github.io/blob/master/cc-cedict_parser/parser.py

		for x in range(len(list_of_dicts)-1, -1, -1):
			if "surname " in list_of_dicts[x]['english']:
				if list_of_dicts[x]['traditional'] == list_of_dicts[x+1]['traditional']:
					list_of_dicts.pop(x)

	def _remove_samples(self, list_of_dicts):
		# takes a dictionary and removes all sample sentences in there
		#   - REGEX: ([\;\/][\s]?Bsp.:[^\;\/]*)(?=[\;\/])
		#   - REGEX: \(Bsp.:[^\)]*\)

		for x in list_of_dicts:
			x['english'] = re.sub(r'([\;\/][\s].Bsp.:[^\;\/]*)(?=[\;\/])', '', x['english'])
			x['english'] = re.sub(r'\(Bsp.:[^\)]*\)', '', x['english'])


	def extendWordlist(self, filename):

		with open(filename) as file:
			wordlist_lines = file.read().splitlines()

			new = list()
			for l in wordlist_lines:
				found = False
				for w in self._dict:
					if w['simplified'] == l:
						found = True
						new.append(l + "\t" + w['pinyin'] + "\t" + w['meaning'])
						break
				if not found:
					new.append(l)
		return new


	def exportCsv(self, filename, export):
		# export a parsed dict and wordlist to a CSV file

		with open(filename, 'w') as file:
			for n in export:
				file.write(n + "\n")

# reload(DictParser)
# dp = DictParser.DictParser()
# dp.loadDict('handedict.u8')
# export = dp.extendWordlist('wordlist.txt')

