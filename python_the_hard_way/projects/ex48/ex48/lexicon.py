class lexicon(object):

    def __init__(self):
      pass

    def scan(self, r):
      result = []
      words = r.split()
      direction_words = {'north', 'south', 'east', 'west', 'down', 'up', 'left', 'right', 'back'}
      verbs = {'go', 'stop', 'kill', 'eat'}
      stop_words = {'the', 'in', 'of', 'from', 'at', 'it'}
      nouns = {'door', 'bear', 'princess', 'cabinet'}
      
      for word in words:
        if word in direction_words:
          t = ('direction', word)
          result.extend([t])
        elif word in verbs:
          t = ('verb', word)
          result.extend([t])
        elif word in stop_words:
          t = ('stop', word)
          result.extend([t])
        elif word in nouns:
          t = ('noun', word)
          result.extend([t])
        else:
          try:
            int(word)
            t = ('number', int(word))
            result.extend([t])
          except:
            t = ('error', word)
            result.extend([t])
        
      return result

