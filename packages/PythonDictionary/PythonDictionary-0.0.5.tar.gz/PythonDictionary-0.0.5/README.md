# PyDictionary
Python wrapper over the Free Dictionary API

```
pip install PyDictionary
```

```python
from PyThonDictionary import pyDictionary

pydictionary = pyDictionary.PyDictionary(word="world")
definitions, synonyms = pydictionary.getDefinitions(partOfSpeech="noun")
audio = pydictionary.getAudio()
dictionary = pydictionary.getDictionary()
```
