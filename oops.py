# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 16:06:58 2021

@author: Isha
"""

import re


# section violations
def getViolations(text):
    violations = re.findall("(violat.*section.*?)\.", text)
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
        
        violations_list = []
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
                
        for i in range(len(violations_list)):
            violation = re.findall("violat.*Section", violations_list[i])
            if violation:
                idx = violations_list[i].find('violat')
                violations_list[i] = violations_list[i][idx:]
            
        #print('\n', violations_list)     
        return violations_list      
    
# violators
def getViolators(text):
    violators = re.findall("v\..*no\.", text)
    if violators:
        for i in range(len(violators)):
            violators[i] = violators[i][3:-5]
            
    #print('\n', violators)
    return violators

# action taken
def actionTaken(text):
    actions = ['settlement', 'penalty', 'court granted', 'admitting or denying the allegations', 'seeks']
    actiontaken = []
    paragraphs = text.split('\n\n')
    for paragraph in paragraphs:
        sentences = paragraph.split('. ')
        flag = False
        for sentence in sentences:
            if flag or any(word in sentence for word in actions): 
                actiontaken.append(sentence.strip())
                flag = True
            
    #print('\n', actiontaken)
    return actiontaken

def main():
    with open('docs/sample9.txt', encoding='utf8') as f:
        text = f.read()
    text = text.lower() 
    
    print('\n\nViolations')
    getViolations(text)
    print('\n\nViolators')
    getViolators(text)
    print('\n\nAction taken')
    actionTaken(text)

if __name__ == "__main__":
    main()    

   
        
