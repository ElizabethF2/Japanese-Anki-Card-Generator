# -*- coding: utf-8 -*-

# Prototype, see JavaScript version instead

separators = '、（）「」０１２３４５６７８９。・ｋｍ'

dictionary = {}

with open('dict.dat', 'rb') as f:
  for line in f:
    line = line.split()
    word = line[0]
    if line[1].startswith('[') and line[1].endswith(']'):
      hirigana = line[1][1:-1]
      definition = ' '.join(line[2:])
    else:
      hirigana = None
      definition = ' '.join(line[1:])
    assert(definition.startswith('/') and definition.endswith('/'))
    definition = definition[1:-1].replace(',', ' ').replace('/(P)', '')
    if hirigana is not None:
      hdefinition = '['+hirigana+'] ' + definition
      if word not in dictionary:
        dictionary[word] = [hdefinition]
      elif hdefinition not in dictionary[word]:
        dictionary[word].append(hdefinition)
      if hirigana not in dictionary:
        dictionary[hirigana] = [definition]
      elif definition not in dictionary[hirigana]:
        dictionary[hirigana].append(definition)
    else:
      if word not in dictionary:
        dictionary[word] = [definition]
      elif definition not in dictionary[word]:
        dictionary[word].append(definition)

def debug_print(msg):
  with open('debug.log','a') as f:
    f.write(msg+'\n')
        
word_frequency = {}

with open('corpus.txt', 'rb') as f:
  for line in f:
    for s in separators:
      line = line.replace(s, ' ')
    for l in line.split():
      debug_print('LINE: ' + l)
      w = l
      while w != '':
        if w in dictionary:
          try: word_frequency[w] += 1
          except KeyError: word_frequency[w] = 1
          l = l[len(w):]
          debug_print('GOT: ' + w)
          debug_print('REM: ' + l)
          w = l 
        else:
          w = w[:-1]

common_words = reversed(sorted(word_frequency.items(), key=lambda kv: kv[1]))
          
with open('output.txt', 'a') as f:
  for word, frequency in common_words:
    f.write('<h1>' + word + '</h1>,' + '<br>'.join(dictionary[word]) + '\n') 

