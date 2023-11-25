# English Assistant Core		 
This project is related to the implementation of the English Assistant Application, which helps us to learn English as an assistant. And, Also this package has the ability to translate from English to Persian.
## Instruction

1. Install [Python](https://www.python.org/).



> ### ⚠ WARNING:
> After install EnglishAssistantCore.
    ```pip install EnglishAssistantCore```, don't forget install *en_core_web_sm* data. ```pip install "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0-py3-none-any.whl"```


2. Install [English Assistant Core](https://github.com/yasharsajadi/EnglishAssistantCore) and [SpaCy-English Core Web Small (en_core_web_sm)](https://github.com/explosion/spacy-models/releases/)

    **Windows:**
    ```
    pip install EnglishAssistantCore & pip install "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0-py3-none-any.whl"
    ```
    **Linux:**
    ```
    pip3 install EnglishAssistantCore && pip3 install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0-py3-none-any.whl
    ```


## Usage

#### Set a string as a list.
```
List = ["Hello"]
#List_String = ["Hello, I am WinCento."]
#List = list(filter(None, re.split(r'\s|\.|,', List_String[0])))
```
#### Set the text.
```
_text = List[0]
```
#### Prepare the core.
```
_core = Core()
```
#### Configurate core.
```
_core.set_voice('en') #language
_core.set_rate(140) #rate
```
#### Speak:
```
_core.speak(_text)
```
#### Record:
```
import os
_core.record(_text,os.path.join(os.path.join(os.path.dirname(__file__)),'output.mp3'))
```
#### Tag With SpaCy:
```
_tag = _core.find_tag_spacy(_text)
_expo = _core.tag_translator_spacy(_tag)
print(_text+" is "+_expo)
```
#### Tag With NLTK (optional):
```
_tag = _core.find_tag_pickle(_text)
_expo = _core.tag_translator_pickle(_tag)
print(_text+" is "+_expo)
```
#### Translate To Persian - Online:
```
_core.set_translator_lang()
_trans = _core.translate_action(_text)
print(_trans)
```
#### Pronunciation:
```
_pron = _core.find_pronunc(list(filter(None, re.split(r'\s|\.|,', _text))))
print(_pron)
```




