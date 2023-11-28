# PyDictionary
Python wrapper over the Free Dictionary API

```
pip install PyDictionary
```

```python
from PyDictionary.PyDictionary import pyDictionary

pydictionary = pyDictionary.PyDictionary(word="world")
definitions, synonyms = pydictionary.getDefinitions(partOfSpeech="noun")
audio = pydictionary.getAudio()
dictionary = pydictionary.getDictionary()
```
