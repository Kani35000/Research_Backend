import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


lemmatizer = WordNetLemmatizer()
stop_words = stopwords.words('english')

def mention_url_notalpha(tweet):
    """
    :param tweet: tweet text
    :return: text
    """
    tweet = re.sub("@[^\s]+"," ", str(tweet))
    tweet = re.sub("http[^\s]+"," ", str(tweet))
    tweet = re.sub(r"[^A-Za-z ]+", " ", str(tweet)) #remove all non-alphabet characters
    tweet = " ".join(tweet.split())  #remove extra spaces, tabs, and new lines
    return tweet


def tokenize_lemma_stopwords(text):
    tokens = word_tokenize(text) # split string into words (tokens)
    tokens = [lemmatizer.lemmatize(t) for t in tokens] # put words into base form
    tokens = [t for t in tokens if len(t) > 2] # remove short words, they're probably not useful
    tokens = [t for t in tokens if t not in stop_words] #NLTK
    tokens = " ".join(tokens)
    return tokens