from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')

def resolve(corenlp_output):
    for coref in corenlp_output['corefs']:
        mentions = corenlp_output['corefs'][coref]
        antecedent = mentions[0] 
        for j in range(1, len(mentions)):
            mention = mentions[j]
            if mention['type'] == 'PRONOMINAL':
                target_sentence = mention['sentNum']
                target_token = mention['startIndex'] - 1
                corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']


def print_resolved(corenlp_output):
    result = ''
    """ Print the "resolved" output """
    possessives = ['hers', 'his', 'their', 'theirs']
    for sentence in corenlp_output['sentences']:
        for token in sentence['tokens']:
            output_word = token['word']
            if token['lemma'] in possessives or token['pos'] == 'PRP$':
                output_word += "'s"
            output_word += token['after']
            print(output_word, end='')
            result += output_word
    return result

def resolve_text(text):
    output = nlp.annotate(text, properties= {'annotators':'dcoref','outputFormat':'json','ner.useSUTime':'false'})
    resolve(output)
    return print_resolved(output)
