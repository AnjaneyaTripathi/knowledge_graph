import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import nltk
from nltk.tokenize import sent_tokenize
import sys

nltk.download('wordnet')
nltk.download('punkt')
stemmer = SnowballStemmer("english")

def load_text(file_name):
    with open(file_name, 'r') as file:
        text = file.read()
    sentences = sent_tokenize(text)
    return sentences

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))   
    return result

def create_bow_dictionary(sentences):
    # preprocessing the sentences by stemming them
    processed_docs = []
    for doc in sentences:
        processed_docs.append(preprocess(doc))
    # forming the dictionary
    dictionary = gensim.corpora.Dictionary(processed_docs)
    # creating the BOWs 
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    return dictionary, bow_corpus

# creating the LDA model
def create_model(topics, bow_corpus, dictionary):
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics = topics, id2word = dictionary, passes = 10, workers = 2)
    return lda_model

# parsing the result of the topics generated
def extract_keywords(s):  
    words=[]
    status=False
    word=''
    for ch in s:
        if(ch=='"'):
            status = not status;
        elif(ch=='+'):
            status=False
            words.append(word)
            word=''
        elif(status):
            word+=ch
    words.append(word)
    return words

def classify_topics(topics, lda_model, sentences):
    keyword_dict = {}
    for i in range(topics):
        keyword_dict[i] = extract_keywords(lda_model.print_topics(-1)[i][1])
    TOPICS = {}
    for i in range(topics):
        TOPICS[i] = []
    for sent in sentences:
        processed = preprocess(sent)
        occurences = [0] * topics
        for word in processed:
            for i in range(topics):
                if(word in keyword_dict[i]):
                    occurences[i]+=1
        top_hit = max(occurences)
        for i in range(topics):
            if(occurences[i]==top_hit):
                TOPICS[i].append(sent)
    return keyword_dict, TOPICS

def get_topics(file_name, topics):
    # enter the name of the file and the number of topics
    sentences = load_text(file_name)
    # create the dictionary and BOW corpus
    dictionary, bow_corpus = create_bow_dictionary(sentences)
    # create the LDA model
    lda_model = create_model(topics, bow_corpus, dictionary)
    # get the keywords of each topic, sentences in each topic
    keyword_dict, TOPICS = classify_topics(topics, lda_model, sentences)
    return TOPICS

if __name__ == '__main__':
    try:
        file_name = sys.argv[1]
        no_of_topics = int(sys.argv[2])
        topics = get_topics(file_name, no_of_topics)
        for i in range(no_of_topics):
            print('\nTopic {}: '.format(i))
            text = " ".join(topics[i])
            print(text, '\n')
                
    except:
        print('Enter correct file name and number of topics')