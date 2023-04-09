from difflib import SequenceMatcher

text = ['anoo', 'd', 'i', 'hals', 'ty', 'jsi', 'm']
end_text= ['anoo', 'd', 'jsi', 'halb', 'ty', 'mi', 'd']



s = SequenceMatcher(None, text, end_text)
similarity = s.ratio()
podobnost_vlastna = 0.6

print (similarity, podobnost_vlastna)