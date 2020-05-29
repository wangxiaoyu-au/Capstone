import re

def lower_folding(x):    
    return x.lower()

# train_sents1_lower.show(5)
def remove_punctuation_re(x):
    x = re.sub(r'[^\w\s]','',x)    
    return x