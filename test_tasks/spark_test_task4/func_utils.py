import re
import argparse

def lower_folding(x):    
    return x.lower()


# train_sents1_lower.show(5)
def remove_punctuation_re(x):
    x = re.sub(r'[^\w\s]','',x)    
    return x


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="the input path",
                        default='~/comp5349/lab_commons/week5/')

    return parser.parse_args()