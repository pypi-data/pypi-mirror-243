import os
import pathlib 
from pathlib import Path
import re

import pyttsx3

import nltk
import pickle
from nltk.corpus import cmudict

import spacy
import en_core_web_sm # https://github.com/explosion/spacy-models/releases/

from googletrans import Translator


# https://stackoverflow.com/questions/2489669/how-do-python-functions-handle-the-types-of-parameters-that-you-pass-in
# https://ieltsliz.com/100-ielts-essay-questions/

class Core() :
    # Initialize
    def __init__(self) -> None:
        self.base_path = os.path.join(os.path.dirname(__file__))
        # self.base_path = Path(__file__).parent
        self.engine = pyttsx3.init()
        self.set_rate(self)
        self.set_voice(self)
        self.tag_loader_pickle()
        self.tag_loader_spacy()
        self.pronunc_loader()

        self.translator = Translator()
        self.translator_lang = self.set_translator_lang(self)

    # Methods    
    def speak(self,text):
        self.engine.say(text)
        self.engine.runAndWait()
        
    def record(self,text,filepath):
        self.engine.save_to_file(text, filepath)
        self.engine.runAndWait()
    
    def set_rate(self,Rate=120):
        self.engine.setProperty('rate', Rate) #rate: 120 ~ 200

    def set_voice(self,lang="en"):
        self.engine.setProperty('voice', lang) #lang: en
    
    def tag_loader_pickle(self):
        nltk.data.path.append(os.path.join(self.base_path+"/nltk_data"))
        file_path = os.path.join(self.base_path+"/nltk_data/taggers/averaged_perceptron_tagger/","averaged_perceptron_tagger.pickle")
        with open(file_path, 'rb') as file:
            self.tagger = pickle.load(file)

    def tag_loader_spacy(self):
        self.nlp = en_core_web_sm.load()
    
    def pronunc_loader(self):
        nltk.data.path.append(os.path.join(self.base_path+"/nltk_data"))

    def tag_translator_pickle(self,InputTag):
        
        ## Make Better
        tag_descriptions = {
            'CC': 'Coordinating conjunction',
            'CD': 'Cardinal number',
            'DT': 'Determiner',
            'EX': 'Existential there',
            'FW': 'Foreign word',
            'IN': 'Preposition or subordinating conjunction',
            'JJ': 'Adjective',
            'JJR': 'Adjective, comparative',
            'JJS': 'Adjective, superlative',
            'LS': 'List item marker',
            'MD': 'Modal',
            'NN': 'Noun, singular or mass',
            'NNS': 'Noun, plural',
            'NNP': 'Proper noun, singular',
            'NNPS': 'Proper noun, plural',
            'PDT': 'Predeterminer',
            'POS': 'Possessive ending',
            'PRP': 'Personal pronoun',
            'PRP$': 'Possessive pronoun',
            'RB': 'Adverb',
            'RBR': 'Adverb, comparative',
            'RBS': 'Adverb, superlative',
            'RP': 'Particle',
            'SYM': 'Symbol',
            'TO': 'to',
            'UH': 'Interjection',
            'VB': 'Verb, base form',
            'VBD': 'Verb, past tense',
            'VBG': 'Verb, gerund or present participle',
            'VBN': 'Verb, past participle',
            'VBP': 'Verb, non-3rd person singular present',
            'VBZ': 'Verb, 3rd person singular present',
            'WDT': 'Wh-determiner',
            'WP': 'Wh-pronoun',
            'WP$': 'Possessive wh-pronoun',
            'WRB': 'Wh-adverb'
            }
        
        if InputTag in tag_descriptions:
            description = tag_descriptions[InputTag]
            return description
        else:
            return "unknown"

    def tag_translator_spacy(self,InputTag):

        tag_descriptions = {
            "ADJ": "Adjective",
            "ADP": "Adposition",
            "ADV": "Adverb",
            "AUX": "Auxiliary verb",
            "CONJ": "Conjunction",
            "CCONJ": "Coordinating conjunction",
            "DET": "Determiner",
            "INTJ": "Interjection",
            "NOUN": "Noun",
            "NUM": "Numeral",
            "PART": "Particle",
            "PRON": "Pronoun",
            "PROPN": "Proper noun",
            "PUNCT": "Punctuation",
            "SCONJ": "Subordinating conjunction",
            "SYM": "Symbol",
            "VERB": "Verb",
            "X": "Other",
            "SPACE": "Space",
        }
        ValidateIndex = self.match_tag_spacy(InputTag) # Make Batter This
        if InputTag[ValidateIndex] in tag_descriptions:
            description = tag_descriptions[InputTag[ValidateIndex]]
            return description
        else:
            return "unknown"

    def pronunc_translator(self,pronunciation):
        arpabet_to_ipa_dict = {
            'AA': 'ɑ:',
            'AE': 'æ',
            'AH0': 'ə', #********
            'AH': 'ʌ',
            'AO': 'ɔ:',
            'AW': 'aʊ',
            'AY': 'aɪ',
            'B': 'b',
            'CH': 'tʃ',
            'D': 'd',
            'DJ': 'dj', # Confuse dew
            'DH': 'ð',
            'EH': 'ɛ',
            'EH1': 'ɪ', #********
            'ER': 'ɜː',
            'ER0': 'ər', #******** ɚ
            'ER2': 'ɜːr', #********
            'EY': 'eɪ',
            'EY2': '', #********
            'F': 'f',
            'G': 'g',
            'HH': 'h',
            'HW': 'hw', # Confuse whine
            'IH': 'ɪ',
            'IH0': 'ə', #******** ɪ
            'IY': 'i:',
            'IY0': 'ə', #********
            'JH': 'dʒ',
            'K': 'k',
            'L': 'l',
            'LU': 'lj', # Confuse lute
            'M': 'm',
            'N': 'n',
            'NG': 'ŋ',
            'NJ': 'nj', # Confuse new
            'OW': 'oʊ',
            'OY': 'ɔɪ',
            'P': 'p',
            'R': 'r',
            'S': 's',
            'SJ': 'sj', # Confuse consume
            'SH': 'ʃ',
            'T': 't',
            'TH': 'θ',
            'TJ': 'θj', # Confuse consume
            'UH': 'ʊ',
            'UW0': 'u', #********
            'UW': 'u:',
            'V': 'v',
            'W': 'w',
            'Y': 'j',
            'Z': 'z', 
            'ZJ': 'zj', # Confuse resume
            'ZH': 'ʒ'
            # ,"1": "'",
            # "2": "ˌ",
            # "0": ".",
        }

        ipa = ''
        for phoneme in pronunciation:
            ipa += arpabet_to_ipa_dict.get(phoneme, '')
        return ipa
   
    def pronunc_stress(self,pronunciation):
        re_pronunciation = []
        for elem in pronunciation :
            i = pronunciation.index(elem)
            if not any(char.isdigit() for char in pronunciation[i]) :
                re_pronunciation.append(elem)
            else :
                re_pronunciation.extend([elem[-1], elem]) if elem in ['AH0', 'ER0', 'ER2', 'UW0' , 'IY0' , 'IH0' , 'EY2' , 'EH1' , 'AO1'] else re_pronunciation.extend([elem[-1], elem[:-1]])
        return re_pronunciation 

    def find_pronunc(self,textList):
        cmu = cmudict.dict()
        ipas = ''
        for word in textList :
            pronunciation_list = cmu.get(word.lower())
            if pronunciation_list :
                
                #British
                # elem0 = pronunciation_list[0]
                # elem0 = stress(elem0)
                # ipa0 = arpabet_to_ipa(elem0)

                #American
                elem1 = pronunciation_list[-1]
                elem1 = self.pronunc_stress(elem1)
                ipa1 = self.pronunc_translator(elem1)

            else:

                Warning("Somthings is wrong.")
                ipa1 = ''
            
            # Add Space
            if word != textList[-1] :
                ipas += ipa1 + ' '
            else :
                ipas += ipa1
        return '/'+ipas+'/'

    def find_tag_pickle(self,text):
        tags = nltk.pos_tag([text])
        tag = tags[0][1]
        return tag
    
    def find_tag_spacy(self,text):
        tags = self.nlp(text)
        taglist = []
        for token in tags:
            taglist.append(token.pos_)
            
        return taglist

    def match_tag_spacy(self,TagList):
        if len(TagList)==2 and (set(TagList) == set(["ADP" , "VERB"]) or set(TagList) == set(["PART" , "VERB"])):
            return TagList.index("VERB")
        else :
            return 0

    def set_translator_lang(self,lang="fa"):
        self.translator_lang = lang ;

    def translate_action(self,text):
        translated_text = self.translator.translate(text, self.translator_lang)
        return translated_text.text

        
        
### Use:

# List = ["Hello, I am WinCento and this is a test message for elluhey, which is written with code and by my own library. This library has the ability to speak 1 languages. and can adjust the speaking rate in it."]
# List = list(filter(None, re.split(r'\s|\.|,', List[0])))
# _text = List[0]

# List = ["Hello"]
# _text = List[0]

# _text = ""
# _core = Core()

## Config
# _core.set_rate(140)
# _core.set_voice('en')

# Speak
# _core.speak(_text)

# Record
# _core.record(_text,os.path.join(os.path.join(os.path.dirname(__file__)),'output.mp3'))

# Tag_pickle
# _tag = _core.find_tag_pickle(_text)
# _expo = _core.tag_translator_pickle(_tag)
# print(_text+" is "+_expo)

# Tag_spacy
# _tag = _core.find_tag_spacy(_text)
# _expo = _core.tag_translator_spacy(_tag)
# print(_text+" is "+_expo)

# Translate - Online
# _core.set_translator_lang()
# _trans = _core.translate_action(_text)
# print(_trans)

# Pronunciation
# _pron = _core.find_pronunc(list(filter(None, re.split(r'\s|\.|,', _text))))
# print(_pron)
