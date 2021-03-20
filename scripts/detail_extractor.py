import re
from nltk.tokenize import sent_tokenize

def getViolations2(text):
    violations_list = getViolations(text)
    for i in range(len(violations_list)):
            violation = re.findall("violat.*Section", violations_list[i])
            if violation:
                idx = violations_list[i].find('violat')
                violations_list[i] = violations_list[i][idx:]
                
    return violations_list

def getViolations3(text):
    sentences = sent_tokenize(text)
    violations_list=[]
    for sentence in sentences:
        violation = re.findall("section.*?of [0-9]{4}", sentence)
        if violation:
            for v in violation:
                violations_list.append(v)
        else:
            violation = re.findall("section.*?act", sentence)
            if violation: 
                for v in violation:
                    violations_list.append(v)
                
    return violations_list

# section violations
def getViolations(text):
    violations = re.findall("(violat.*section.*?)\.", text)
    violations_list = []
    if violations:
        z = re.split('section',violations[0])
        for i in range(len(z)):
            if i>0:
                z[i] = 'Section' + z[i]
        y = []
        for item in z:
            t = re.split('\. ', item)
            for sent in t:
                y.append(sent)
        y[1] = y[0] + y[1]
        
        for i in range(1, len(y), 1):
            nums = re.findall(r'[0-9]+', y[i])            
            if not nums:
                y[i+1] = y[i] + y[i+1]
                #violations_list.append(y[i] + y[i+1])
            #elif i!=1:
            else:
                idx = y[i].find('thereunder')
                if(idx!=-1):
                    violations_list.append(y[i][:idx+10])
                    if not i==len(y)-1:
                        if not (len(y[i])<idx+12):
                            y[i+1] = y[i][idx+12:] + y[i+1]
                else:
                    violations_list.append(y[i])
            
            l = len(violations_list)
            z = violations_list[l-1].rfind("and")
            if z!=-1:
                penalty = violations_list[l-1].rfind("$", z)
                section = violations_list[l-1].rfind("Section", z)
                if penalty!= -1 and section==-1:
                    violations_list[l-1] = violations_list[l-1][:z]
                    
        for i in range(len(violations_list)):
            if violations_list[i].startswith('and'):
                violations_list[i] = violations_list[i][4:]
            if violations_list[i].endswith('and '):
                violations_list[i] = violations_list[i][:-4]
                 
    return violations_list      
    
# violators
def getViolators(text):
    violators = re.findall("v\..*no\.", text)
    violators_list=[]
    if violators:
        violators = violators[0][3:-5]
    else:
        violators = re.findall("v\..*?[0-9]", text)
        if violators:
            violators = violators[0][3:-5]
    if violators:        
        result = [x.strip() for x in violators.split(',')] 
        for res in result:
            if(len(res)>7):
                violators_list.append(res)
                if(res=='et al.'):
                    break

    return violators_list

# action taken
def actionTaken(text):
    actions = ['settlement', 'penalty', 'court granted', 'admitting or denying the allegations']
    actiontaken = []
    paragraphs = text.split('\n\n')
    for paragraph in paragraphs:
        sentences = paragraph.split('. ')
        flag = False
        for sentence in sentences:
            if flag or any(word in sentence for word in actions): 
                actiontaken.append(sentence.strip())
                flag = True
            
    return actiontaken

def multiKeywords(keywords, sentence, label_index):
    res = [ele for ele in keywords if(ele in sentence)]
    if(len(res)>1):
        return True
    return False

def getAllPenalties(text):
    sentences = sent_tokenize(text)
    penalties=[]
    for sentence in sentences:
        getPenalty(penalties, sentence)  
    return penalties

def findAmount(snippet):
    num = re.findall(r'\d+', snippet)[-1]
    start = snippet.rfind('$')
    end = snippet.rfind(num)
    return start, end+len(num)

def getPenalty(penalties, text):
    labels = ['Disgorgement', 'Penalty', 'Prejudgment interest', 'Total']
    keywords = ['disgorge', 'penalt', 'prejudgment interest', ]
        
    # Disgorgement
    disgorge_regex1 = re.findall('\$.*?in disgorge', text)
    if disgorge_regex1:
        for disgorgement in disgorge_regex1:
            if not (multiKeywords(keywords, disgorgement, 0)):
                start, end = findAmount(disgorgement)
                penalties.append([labels[0], disgorgement[start:end]])
    disgorge_regex2 = re.findall('disgorge.*?of \$.*?[ \.]', text)
    if disgorge_regex2:
        for disgorgement in disgorge_regex2:
            if not (multiKeywords(keywords, disgorgement, 0)):
                start, end = findAmount(disgorgement)
                penalties.append([labels[0], disgorgement[start:end]])
            
    # # Civil Penalty
    # civil_regex1 = re.findall('\$.*?in civil penalt', text)
    # if civil_regex1:
    #     for civil_penalty in civil_regex1:
    #         start, end = findAmount(civil_penalty)
    #         penalties.append([labels[1], civil_penalty[start:end]])
    # civil_regex2 = re.findall('civil penalt.*?of \$.*?[ \.]', text)
    # if civil_regex2:
    #     for civil_penalty in civil_regex2:
    #         start, end = findAmount(civil_penalty)
    #         penalties.append([labels[1], civil_penalty[start:end]])
            
    # Penalty
    penalty_regex1 = re.findall('\$.*?in.*?penalt', text)
    if penalty_regex1:
        for penalty in penalty_regex1:
            if not (multiKeywords(keywords, penalty, 1)):
                start, end = findAmount(penalty)
                penalties.append([labels[1], penalty[start:end]])
    penalty_regex2 = re.findall('penalt.*?\$.*?[ \.]', text)
    if penalty_regex2:
        for penalty in penalty_regex2:
            if not (multiKeywords(keywords, penalty, 1)):
                start, end = findAmount(penalty)
                penalties.append([labels[1], penalty[start:end]])
            
    # Prejudgement interest
    prejudgment_regex1 = re.findall('\$.*?in prejudgment interest', text)
    if prejudgment_regex1:
        for interest in prejudgment_regex1:
            if not (multiKeywords(keywords, interest, 2)):
                start, end = findAmount(interest)
                penalties.append([labels[2], interest[start:end]])
    prejudgment_regex2 = re.findall('prejudgment interest.*?of \$.*?[ \.]', text)
    if prejudgment_regex2:
        for interest in prejudgment_regex2:
            if not (multiKeywords(keywords, interest, 2)):
                start, end = findAmount(interest)
                penalties.append([labels[2], interest[start:end]])
            
    # Total
    total_regex = re.findall('total.*?\$.*?[ \.]', text)
    if total_regex:
        for total in total_regex:
            start, end = findAmount(total)
            penalties.append([labels[3], total[start:end]])
    
    return penalties

def getDate(text):
    year = ''
    dt = ''
    date = re.findall("[a-z]* [0-9]+, [0-9]{4}", text)
    if(date):
        # date = re.findall("[a-z]* [0-9]+, [0-9]{4}", date[0])
        year = date[0][-4:]
        dt = date[0]
    return dt, year

def main():
    with open('docs/sample18.txt', encoding='utf8') as f:
        text = f.read()
    
    # print('\n\nViolations')
    # getViolations3(text)
    # print()
    text = text.lower() 

    # getViolations2(text)
    # print('\n\nViolators')
    # getViolators(text)
    # print('\n\nAction taken')
    # actionTaken(text)
    
    print('\n\n Penalty')
    getAllPenalties(text)
    
if __name__ == "__main__":
    main()    

   
        
