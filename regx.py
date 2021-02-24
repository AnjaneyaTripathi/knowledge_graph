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
        y = re.split('section',violations[0])
        for i in range(len(y)):
            if i>0:
                y[i] = 'Section' + y[i]
        violations_list = []
        for i in range(len(y)):
            nums = re.findall(r'[0-9]+', y[i])            
            if not nums:
                violations_list.append(y[i] + y[i+1])
            elif i!=1:
                idx = y[i].find('thereunder, ')
                if(idx!=-1):
                    violations_list.append(y[i][:idx+10])
                    y[i+1] = y[i][idx+12:] + y[i+1]
                else:
                    violations_list.append(y[i])
    
        for i in range(len(violations_list)):
            if violations_list[i].startswith('and'):
                violations_list[i] = violations_list[i][4:]
            if violations_list[i].endswith('and '):
                violations_list[i] = violations_list[i][:-4]
            
        print('\n', violations_list)           
    
# violators
def getViolators(text):
    violators = re.findall("v\..*no\.", text)
    if violators:
        for i in range(len(violators)):
            violators[i] = violators[i][3:-5]
            
    print('\n', violators)

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
            
    print('\n', actiontaken)

def main():
    with open('./docs/regex3.txt', encoding='utf8') as f:
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

   
        
