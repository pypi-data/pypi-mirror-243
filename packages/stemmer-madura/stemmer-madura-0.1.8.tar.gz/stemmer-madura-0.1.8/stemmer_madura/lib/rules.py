import re

# Rule class
class Rule:
  def __init__(self, name, pattern, replacement, replacements, recover):
    self.name = name
    self.pattern = pattern
    self.replacement = replacement
    self.replacements = replacements
    self.recover = recover

rules = [
  # Reduplication Removal
  Rule(
    'Reduplication Removal',
    re.compile(r'^.+\-(.+)$'),
    r'\1',
    [],
    False
  ),




  # Nah Suffix Removal
  # Sepertinya tidak baku, mungkin bentuk dari akhiran "na" (romana, kalambina)
  Rule(
    'Nah Suffix Removal',
    re.compile(r'^(.+)nah$'),
    r'\1',
    [],
    True
  ),

  # Han Suffix Removal
  # Beberapa kata dengan akhiran konsonan + han (katorodhan, kawajibhan)
  Rule(
    'Han Suffix Removal',
    re.compile(r'^(.+)han$'),
    r'\1',
    [],
    'both'
  ),
  
  # Plain Suffix Removal 1
  Rule(
    'Plain Suffix Removal 1',
    re.compile(r'^(.+)(ya|na|ni|an|ih|eh|en|ah)$'),
    r'\1',
    [],
    'both'
  ),

  # Plain Suffix Removal 2
  Rule(
    'Plain Suffix Removal 2',
    re.compile(r'^(.+)([aei])$'),
    r'\1',
    [],
    'both'
  ),

  # Aghi Suffix Removal
  Rule(
    'Aghi Suffix Removal',
    re.compile(r'^(.+)aghi$'),
    r'\1',
    [],
    False
  ),



  # Plain Prefix Removal 1
  Rule(
    'Plain Prefix Removal 1',
    re.compile(r'^([ae])(.+)$'),
    r'\2',
    [],
    False
  ),

  # Plain Prefix Removal 2
  Rule(
    'Plain Prefix Removal 2',
    re.compile(r'^(ta|ma|ka|sa|pa|pe)(.+)$'),
    r'\2',
    [],
    'both'
  ),

  # Plain Prefix Removal 3
  Rule(
    'Plain Prefix Removal 3',
    re.compile(r'^(par)([^aeuio].+)$'),
    r'\2',
    [],
    False
  ),

  # Ng Prefix Removal 1
  Rule(
    'Ng Prefix Removal 1',
    re.compile(r'^ng(.+)$'),
    r'\1',
    [],
    True
  ),

  # Ng Prefix Modification 2
  Rule(
    'Ng Prefix Modification 2',
    re.compile(r'^ng([aeio].+)$'),
    '',
    [r'k\1', r'g\1', r'gh\1'],
    False
  ),

  # M Prefix Modification
  Rule(
    'M Prefix Modification',
    re.compile(r'^m([aeou].+)$'),
    '',
    [r'b\1', r'p\1', r'bh\1'],
    False
  ),

  # NY Prefix Modification
  Rule(
    'NY Prefix Modification',
    re.compile(r'^ny([aeo].+)$'),
    '',
    [r's\1', r'c\1', r'j\1', r'jh\1'],
    False
  ),

  # N Prefix Modification
  Rule(
    'N Prefix Modification',
    re.compile(r'^n([aeo].+)$'),
    '',
    [r't\1', r'd\1', r'dh\1'],
    False
  ),


  # Gha Suffix Modification (tabhaligha, sabhaligha), morph gha to k
  Rule(
    'Gha Suffix Modification',
    re.compile(r'^(.+)(gha)$'),
    r'\1k',
    [],
    False
  ),

  # Dhan Suffix Removal (katorodhan)
  Rule(
    'Dhan Suffix Removal',
    re.compile(r'^(.+)dhan$'),
    r'\1t',
    [],
    False
  ),
  

  # Plain Infix Removal
  Rule(
    'Plain Infix Removal',
    re.compile(r'^([^aiueo]{1,2})(al|ar|en|in|om|um)(.+)$'),
    r'\1\3',
    [],
    False
  )
]

