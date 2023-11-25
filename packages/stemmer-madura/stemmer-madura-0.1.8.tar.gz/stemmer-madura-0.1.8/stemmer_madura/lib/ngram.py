class NGram:
  def __init__(self, firstWord, secondWord, n=2):
    self._firstWord = firstWord
    self._secondWord = secondWord
    self._gram = n
    self.firstGrams = []
    self.secondGrams = []

  def calculate(self):
    self.firstGrams = self.generateGrams(f'*{self._firstWord}*')
    self.secondGrams = self.generateGrams(f'*{self._secondWord}*')
    shared = 0
    for fg in self.firstGrams:
      for sg in self.secondGrams:
        if fg == sg:
          shared += 1
    return round((2 * shared) / (len(self.firstGrams) + len(self.secondGrams)), 3)

  def generateGrams(self, word):
    r = []
    for i in range(len(word) - 1):
      e = word[i:i+self._gram]
      r.append(e)
    return r
