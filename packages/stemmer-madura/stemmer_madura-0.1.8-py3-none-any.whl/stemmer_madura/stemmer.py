import re
from typing import List
from .lib.stemmer import Stemmer
import os

class _Files:
  """
  A class that provides methods to read files and split their contents into words.

  Attributes:
  stemmer (Stemmer): A Stemmer object used to normalize the words in the file.

  Methods:
  readFile(filename: str) -> List[str]: Reads the contents of the file and splits it into words.
  """
  def __init__(self, stemmer: Stemmer):
    self._stemmer = stemmer

  @property
  def stemmer(self) -> Stemmer:
    return self._stemmer
  
  def readFile(self, filename: str) -> List[str]:
    with open(filename, 'r', encoding="utf-8") as file:
      return self._splitWordsFile(file.read())
    

  def _splitWordsFile(self, content: str) -> List[str]:
    lf = self._getLineBreakChar(content)
    result = []
    for v in content.split(lf):
      if len(v) > 0:
        normalized = self._stemmer.normalizeString(v, True)
        # Check if the word has a variant (h)
        match = re.match(r'(.+)\(h\)$', normalized)
        # If it has a variant, add both the word and its variant
        if match:
          result.append(match.group(1))
          result.append(match.group(1) + 'h')
        else:
          result.append(normalized)
    return result

  def _getLineBreakChar(self, content: str) -> str:
    index_of_lf = content.find('\n', 1)  # No need to check first-character
    if index_of_lf == -1:
      if '\r' in content:
        return '\r'
      return '\n'
    if content[index_of_lf - 1] == '\r':
      return '\r\n'
    return '\n'


def stemmer(word: str, verbose = False, withNgram: bool = False, ngGramThreshold: int = 0.5) -> str:
  """
  Stem a given word using the Madura stemmer algorithm.

  Args:
    word (str): The word to be stemmed.
    verbose (bool, optional): Whether to print the logs. Defaults to False.
    withNgram (bool, optional): Whether to use n-gram matching. Defaults to False.
    ngGramThreshold (int, optional): The threshold for n-gram matching. Defaults to 0.5.

  Returns:
    str: The stemmed word.
  """
  stemmer = Stemmer()
  stemmer.input = word
  if verbose:
    stemmer.verbose = True
  
  if withNgram:
    stemmer.withNgram = withNgram
    stemmer.ngGramThreshold = ngGramThreshold

  file = _Files(stemmer)
  module_dir = os.path.dirname(__file__)
  stemmer.baseWords = file.readFile(os.path.join(module_dir, 'data/lemmawords.txt'))
  stemmer.stopWords = file.readFile(os.path.join(module_dir, 'data/stopwords.txt'))
  
  stemmed = stemmer.stemWords()
  if verbose:
    # dump content of fullLogs
    for log in stemmer.fullLogs:
      for l in log:
        print(l)

  return stemmed
  
