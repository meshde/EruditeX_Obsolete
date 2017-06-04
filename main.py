import time
start = time.time()
import spacy
from erudite import Interpres

nlp = spacy.load('en')
mid = time.time()
sent = 'John gave Mary a book'

doc = nlp(sent)
print(Interpres.translate(doc).__dict__)
end = time.time()
print('Time to load Spacy and NLTK:\t'+str(mid-start))
print('Executuion time:\t'+str(end-mid))