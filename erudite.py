import spacy
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import pywsd
import sys
class Person(object):
	def __init__(self,name):
		self.name = name
		self.gender = Person.getGender(name) ####FIND OUT!!!!!!!!!!!!!!
		self.height = Person.getHeight(self.gender) #######DEFINE for avg male and female height
		self.weight = Person.getWeight(self.gender) #######DEFINE for avg weight 
		self.age = 25
		self.profession = ''
		self.health = 100
		self.residence = '' #########PPLEASE CONFIRM
		self.emotionalState = 100
	@staticmethod
	def getHeight(gender):
		"""Height in cm"""
		if gender.upper() == 'MALE':
			return 165
		return 152
	@staticmethod
	def getWeight(gender):
		"""Weight in kg"""
		if gender.upper() == 'MALE':
			return 80
		return 50
	@staticmethod
	def getGender(name):
		return 'MALE'


class PTRANS(object):
	def __init__(self,verb,context):
		self.verb = verb.text
		self.doer = Interpres.getEntity([z for z in verb.children if z.dep_ == 'nsubj'][0]).__dict__
		self.receiver = Interpres.getEntity([z for z in verb.children if z.dep_ == 'dobj' and z.ent_type_ == 'PERSON'][0]).__dict__
		self.object = Interpres.wsd(context,[z for z in verb.children if z.dep_ == 'dobj' and z.ent_type_ != 'PERSON'][0],'lesk')


class Interpres(object):
	@staticmethod
	def translate(sentence):
		root = [z for z in sentence if z.head == z]
		root = root[0]
		concept = Interpres.map_get(Interpres.wsd(sentence.text,root,'lesk')._name)
		concept = Interpres.getConcept(concept,root,sentence)
		return concept
	@staticmethod
	def map_get(verb):
		with open('map.txt','r') as f:
			flag = 0
			for line in f:
				lhs,rhs = line.strip().split()
				if lhs == verb:
					flag = 1
					break
		if flag == 1:
			return rhs
		else:
			""" Raise Error """
			sys.stderr.write("Sorry, my creators didn't bother to tell me what "+verb+" means")
			sys.exit(0)
	@staticmethod
	def getConcept(concept,verb,context):
		if concept == 'PTRANS':
			return PTRANS(verb,context)
	@staticmethod
	def getEntity(noun):
		try:
			#root = chunk.root
			entity_type = noun.ent_type_
			if entity_type == 'PERSON':
				p = Person(noun.text)
				for c in noun.children:
					if c.pos_ == 'DET':
						""" Complete Later """
					elif c.pos_ == '':
						""" Complete Later """
				return p
			else:
				"""Complete Later"""
		except:
			print('What the fuck?')
			pass
		return
	@staticmethod
	def getNLTKpos(pos):
		"""Converting spacy POS to nltk POS"""
		if pos == 'NOUN' or pos == 'PROPN':
			return 'n'
		if pos == 'VERB':
			return 'v'
	@staticmethod
	def wsd(context,word,typ):
		"""Word Sense Disambiguation to find the correct sense of a given word in context"""
		try:
			context = context.text
		except:
			pass
		synsets = wordnet.synsets(word.text,Interpres.getNLTKpos(word.pos_))
		if typ == 'lesk':
			rankings = Interpres.lesk(context,synsets) ###### Using inaccurate and unreliable lesk algo only FOR NOW
			return synsets[rankings.index(max(rankings))]
		if typ == 'pywsd':
			return pywsd.lesk.simple_lesk(context,word.text)
		if typ == 'pywsd.cos':
			return pywsd.lesk.cosine_lesk(conetxt,word.text)
	@staticmethod
	def lesk(context,synsets):
		"""Checks no of overlapping words in examples of each synset with the context"""
		ranking = [0 for z in synsets]
		stop = stopwords.words('english')
		context_set = set(z.lower() for z in context.split() if z.lower() not in stop) #### Change context.split() to something more reliable
		for i,syn in enumerate(synsets):
			maxi = 0
			for example in syn.examples():
				synset = set(z.lower() for z in example.split() if z.lower() not in stop) #### Confirm working of example.split()
				average_length = (len(context_set) + len(synset)) / 2
				points = len(context_set.intersection(synset)) / average_length
				maxi = max(maxi,points)
			ranking[i] = maxi
		return ranking
