import requests
from .constants import API_URL

class PyDictionary:
    def __init__(self, word):
        self.word = word
    
    def getDictionary(self):
        return requests.get(API_URL + self.word).json()
    
    def getDefinitions(self, partOfSpeech):
        
        self.partOfSpeech = partOfSpeech
        
        meanings = self.getDictionary()
        definitions = []
        synonyms = []
        for x in meanings:
            if x['meanings'][0]['partOfSpeech'] == self.partOfSpeech:
                for y in x['meanings'][0]['definitions']:
                    definitions.append(y['definition'])
                    synonyms.append(y['synonyms'])
                    
        return definitions, synonyms
        
    def getAudio(self):
        
        audios = self.getDictionary()[0]["phonetics"]
        audio_urls = []
        for a in audios:
            audio_urls.append(a['audio'])
        return audio_urls
