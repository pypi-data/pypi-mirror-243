from typing import List
import re
from .ngram import NGram
from .rules import rules
import unicodedata

class Stemmer:
  def __init__(self):
    self._verbose: bool = False
    self._logs: List[str] = []
    self._fullLogs: List[List[str]] = []
    self._input: str = ''
    self._success: bool = False
    self._withNgram: bool = False
    self._ngGramThreshold: float = 0.66
    self._words: List[str] = []
    self._results: List[str] = []
    self._originalWord: str = ''
    self._ruleIndex: int = -1
    self._currentWords: List[str] = []
    self._bagOfResults: List[str] = []

  @property
  def verbose(self) -> bool:
    return self._verbose

  @verbose.setter
  def verbose(self, val: bool) -> None:
    self._verbose = val

  @property
  def fullLogs(self) -> List[List[str]]:
    return self._fullLogs

  @property
  def input(self) -> str:
    return self._input

  @input.setter
  def input(self, val: str) -> None:
    if len(val) > 0:
      self._input = self.normalizeString(val)
    else:
      raise ValueError(401)

  @property
  def isSuccess(self) -> bool:
    return self._success

  @property
  def withNgram(self) -> bool:
    return self._withNgram

  @withNgram.setter
  def withNgram(self, mode: bool) -> None:
    self._withNgram = mode

  @property
  def ngGramThreshold(self) -> float:
    return self._ngGramThreshold

  @ngGramThreshold.setter
  def ngGramThreshold(self, threshold: float) -> None:
    self._ngGramThreshold = threshold

  def addLog(self, log: str) -> None:
    if self._verbose:
      self._logs.append(log)

  def dumpLogs(self) -> None:
    if self._verbose:
      if len(self._logs) > 0:
        self._fullLogs.append(self._logs)
        self._logs = []
  

  def stemWord(self, word: str) -> str:
    self._originalWord = word
    self._currentWords = [word]
    self._ruleIndex = 0
    self._bagOfResults = []

    self.addLog(f'⚡ Memproses kata "{word}"')

    if self.inBaseWords(word):
      self._success = True
      self.addLog(f'⭐ Menemukan kata "{word}" untuk kata "{word}" di kata dasar')
      self.dumpLogs()
      self._bagOfResults.append(word)

    while True:
      rule = rules[self._ruleIndex]

      recheckCurrentWords = False
      for k in range(len(self._currentWords)):
        w = self._currentWords[k]

        if rule.pattern.search(w):
          self.addLog(f'⇨ Menjalankan rule "{rule.name}" pada kata "{w}"')

          # If the rule replacements length == 0), just replace the word
          if len(rule.replacements) == 0:
            morph = rule.pattern.sub(rule.replacement, w)
            self.addLog(f'⇨ Mengubah kata "{w}" menjadi: "{morph}"')

            if self.inBaseWords(morph):
              self._success = True
              self.addLog(f'⭐ Menemukan kata "{morph}" untuk kata "{word}" di kata dasar')
              self.dumpLogs()
              self._bagOfResults.append(morph)
            else:
              if rule.recover:
                self.addLog(f'⇨ Mengembalikan kata "{morph}" ke "{w}"')
                self._currentWords[k] = w
                if rule.recover == 'both':
                  self._currentWords.append(morph)
              else:
                self._currentWords[k] = morph
          else:
            morphs = []
            for r in rule.replacements:
              morph = rule.pattern.sub(r, w)
              self.addLog(f'⇨ Mengubah kata "{w}" menjadi: "{morph}"')
              if self.inBaseWords(morph):
                self._success = True
                self.addLog(f'⭐ Menemukan kata "{morph}" untuk kata "{word}" di kata dasar')
                self.dumpLogs()
                self._bagOfResults.append(morph)
                
              morphs.append(morph)
            self._currentWords.pop(k)
            self._currentWords += morphs
            recheckCurrentWords = True
            break

      if not recheckCurrentWords:
        self._ruleIndex += 1

      if self._ruleIndex == len(rules):
        break

    if self._withNgram:
      for baseWord in self._baseWords:
        nGram = NGram(baseWord, word)
        value = nGram.calculate()

        if value >= self._ngGramThreshold:
          self._success = True
          self.addLog(f'⭐ Menemukan kata "{baseWord}" untuk kata "{word}" di kata dasar menggunakan N-Gram')
          self.dumpLogs()
          self._bagOfResults.append(baseWord)

    self.addLog(f'⚠ Tidak dapat menemukan kata "{word}" di kata dasar')
    self.dumpLogs()
    # if len of bagOfResults > 0, return all the results joined by /
    if len(self._bagOfResults) > 0:
      return '/'.join(self._bagOfResults)
    return self._originalWord

  def stemWords(self) -> str:
    self._fullLogs = []
    
    self._words = re.findall(r'\b[\w-]+\b', self._input)
    self.addLog(f'✔ Tokenisasi input: "{self._input}" menjadi: [{", ".join(self._words)}]')

    self._results = [self.normalizeString(word) for word in self._words]
    self.addLog(f'✔ Proses casefolding menjadi: [{", ".join(self._results)}]')

    self._results = [v for v in self._results if not self.inStopWords(v) and len(v) > 2]
    self.addLog(f'✔ Proses pembuangan stopwords menjadi: [{", ".join(self._results)}]')
    self.dumpLogs()

    if len(self._results) > 0:
      self._results = [self.stemWord(word) for word in self._results]
      return ' '.join(self._results)
    return ''

  def normalizeString(self, text: str, fromDict: bool = False) -> str:
    # normalize the text to NFD form
    text = unicodedata.normalize('NFD', text)

    # remove diacritics
    text = re.sub(r'[\u0300-\u036f]', '', text)

    # remove non-alphabet characters, hypens, single quotes, and spaces
    if not fromDict:
      text = re.sub(r'[^a-zA-Z\-\' ]', '', text)
    else:
      text = re.sub(r'[^a-zA-Z\-\'\(\) ]', '', text)

    # convert to lowercase and strip leading and trailing spaces
    text = text.strip().lower()

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text

  @property
  def baseWords(self) -> List[str]:
    return self._baseWords

  @baseWords.setter
  def baseWords(self, words: List[str]) -> None:
    self._baseWords = words

  def inBaseWords(self, word: str) -> bool:
    if (self._verbose):
      self.addLog(f'⇨ Mencari kata "{word}" di kata dasar')
    return word in self._baseWords

  @property
  def stopWords(self) -> List[str]:
    return self._stopWords

  @stopWords.setter
  def stopWords(self, words: List[str]) -> None:
    self._stopWords = words

  def inStopWords(self, word: str) -> bool:
    return word in self._stopWords