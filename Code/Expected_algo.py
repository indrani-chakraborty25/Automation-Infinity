'''
    File name: Expected_algo.py
    Author: Indrani/Geerisha
    Date created: 25/03/2021
    Date last modified: 21/05/2021
    Python Version: 3.6.8
    Description: It contains the algorithm/code for populating Test Case documents with Expected Results

'''

import spacy                                                    #Importing Packages
import string
from csv import DictReader
import csv
import re
from nltk.tokenize import sent_tokenize
import language_check



def find_index(part_of_speech_1,input_string):                  #Function to Find the first and last occurance of a Noun/Proper Noun in a sentence
    first_index = 0
    last_index = 0
    last_index_noun = 0
    first_index = part_of_speech_1.index('NOUN')                
    part_of_speech_1.reverse()                                  #Reverse the list to find the last occurance
    last_index_noun = part_of_speech_1.index('NOUN')            
    if last_index_noun == 0:                                    #If last word in a sentence is a Noun/Proper Noun
        last_index = len(input_string)
    else:                                                       #Find the last index
        last_index = len(part_of_speech_1)- part_of_speech_1.index('NOUN')

    return(first_index,last_index)                              #Function returns the first and last Index

def count_nouns(part_of_speech_1):                              #Counts the number of Nouns/Proper Nouns in a sentence

    count_noun = 0
    for pos in part_of_speech_1:
        if pos=='NOUN':
            count_noun= count_noun+1
    return(count_noun)                                          #Function returns the count

def extraction_1(part_of_speech_1,input_string,output,first_index): #Find if the sentence indicates any action performed by the object

    verb_index =0
    verb_word = ''
    new_verb = ''
    text = ''
    length = len(input_string)
    verb_index = part_of_speech_1.index('VERB')
    if (verb_index>=0 and verb_index<=length and verb_index<first_index): #If the action is not already extracted, find the action performed
        verb_word = input_string[verb_index]
        for j in range(first_index, len(input_string)):                    #Extracting information from Sentences
            output=output+input_string[j]+" "
        if verb_word=='Open' or verb_word=='Select':
            output= output+'should be '+verb_word+'ed'
        elif verb_word=='Close' or verb_word=='Save':
            output=output+'should be '+verb_word+'d'
        else:
            text = 'should be '+verb_word
            tool = language_check.LanguageTool('en-US')
            matches = tool.check(text)
            output = output+(language_check.correct(text,matches))

    else:
        for j in range(first_index, len(input_string)):
            output=output+input_string[j]+" "

    return(output)

def extraction_2(part_of_speech_1,input_string,output,first_index):     #Find if the sentence indicates any action performed by the object

    adj_index =0
    verb_word = ''
    new_verb = ''
    text = ''
    length = len(input_string)
    adj_index = part_of_speech_1.index('ADJ')
    if (adj_index>=0 and adj_index<=length and adj_index<first_index):
        verb_word = input_string[adj_index]
        for j in range(first_index, len(input_string)):
            output=output+input_string[j]+" "
        if verb_word=='Open' or verb_word=='Select':
            output= output+'should be '+verb_word+'ed'
        elif verb_word=='Close' or verb_word=='Save':
            output=output+'should be '+verb_word+'d'
        else:
            text = 'should be '+verb_word
            tool = language_check.LanguageTool('en-US')
            matches = tool.check(text)
            output = output+(language_check.correct(text,matches))
    else:
        for j in range(first_index, len(input_string)):
            output=output+input_string[j]+" "

    return(output)

def extraction_3(part_of_speech_1,input_string,output,first_index,last_index):

    verb_index =0
    verb_word = ''
    new_verb = ''
    text = ''
    length = len(input_string)
    verb_index = part_of_speech_1.index('VERB')
    if (verb_index>=0 and verb_index<=length and (verb_index<first_index or verb_index>last_index)):
        try:
            verb_word = input_string[verb_index]
            for j in range(first_index, len(input_string)):
                output=output+input_string[j]+" "
            if verb_word=='Open' or verb_word=='Select':
                output= output+'should be '+verb_word+'ed'
            elif verb_word=='Close' or verb_word=='Save':
                output=output+'should be '+verb_word+'d'
            else:
                text = 'should be '+verb_word
                tool = language_check.LanguageTool('en-US')
                matches = tool.check(text)
                output = output+(language_check.correct(text,matches))
        except:
            output = output+input_string
    else:
        for j in range(first_index, len(input_string)):
            output=output+input_string[j]+" "

    return(output)

def extraction_4(part_of_speech_1,input_string,output,first_index,last_index):

    adj_index =0
    verb_word = ''
    new_verb = ''
    text = ''
    length = len(input_string)
    if 'ADJ' in part_of_speech_1:
        adj_index = part_of_speech_1.index('ADJ')
        if (adj_index>=0 and adj_index<=length and adj_index<first_index):
            verb_word = input_string[adj_index]
            for j in range(first_index, len(input_string)):
                output=output+input_string[j]+" "
            if verb_word=='Open' or verb_word=='Select':
                output= output+'should be '+verb_word+'ed'
            elif verb_word=='Close' or verb_word=='Save':
                output=output+'should be '+verb_word+'d'
            else:
                text = 'should be '+verb_word
                tool = language_check.LanguageTool('en-US')
                matches = tool.check(text)
                output = output+(language_check.correct(text,matches))
        else:
            for j in range(first_index, len(input_string)):
                output=output+input_string[j]+" "
    else:
        for j in range(first_index, len(input_string)):
            output=output+input_string[j]+" "

    return(output)


def extract_information(part_of_speech_1,input_string,output,count):

    first_index,last_index = find_index(part_of_speech_1,input_string)
    count_noun = count_nouns(part_of_speech_1)
    
    verb_index =0
    adj_index=0
    new_verb = ''
    length = len(input_string)
    part_of_speech_1.reverse()
                    
    if count_noun==1:
        if 'VERB' in part_of_speech_1:
            output = extraction_1(part_of_speech_1,input_string,output,first_index)   
        else:
            if 'ADJ' in part_of_speech_1:
                output = extraction_2(part_of_speech_1,input_string,output,first_index)
            else:
                for j in range(first_index, len(input_string)):
                    output=output+input_string[j]+" "

        return(output)

    else:
        if 'VERB' in part_of_speech_1:
            output = extraction_3(part_of_speech_1,input_string,output,first_index,last_index)
        else:
            output = extraction_4(part_of_speech_1,input_string,output,first_index,last_index)

        return(output)
            
def main():
    count=1
    FieldNameSLNo = "SLNo"
    FieldNameExpectedResult = "Expected Result"
    with open('Output_Expected_Results.csv', mode='w') as csv_file:
        fieldnames = [FieldNameSLNo,FieldNameExpectedResult]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n') 
        writer.writeheader()
        writer.writerow({FieldNameSLNo:'1',FieldNameExpectedResult: "Successfully Reads All The Data In The Config File And Stores It In The Collection And Delete The File"})

    with open('Dataset_TestCase.csv', 'r') as read_obj:                                   
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            count+=1         
            output = '' 
            expected_res = ''                                                         
            raw_text= row['Step'].strip()
            nlp = spacy.load('en_core_web_sm')
            raw_text_list = sent_tokenize(raw_text)
            
            local_count=1
            if count>1:                                                        #Identifying the Pre-Requisites
                expected_res= expected_res+'Pre-requisite:- Bot/user has successfully completed step '+str(count-1)+'.'+'\n'
            for text in raw_text_list:
                text= text.strip(".")
                doc = nlp(text)
                text = string.capwords(text)
                part_of_speech=[]
                conjuction = 'CCONJ'
                input_string= text.split(" ")
                for token in doc:
                    part_of_speech.append(token.pos_)
                part_of_speech_2=[]
                for pos in part_of_speech:
                    if pos=='PROPN':
                        part_of_speech_2.append('NOUN')
                    else:
                        part_of_speech_2.append(pos)
                part_of_speech_1=[]
                for p in part_of_speech_2:
                    if p!='PUNCT':
                        part_of_speech_1.append(p)
                words = ['In','On','After','If','Else']
                res = [i for i in words if(i in text)]
                if str(bool(res))=='True':
                    expected_res = expected_res+str(local_count)+'. '+text +'.'+'\n'
                elif text.startswith('Go') or conjuction in part_of_speech_1 or text.startswith('Wait'):
                    expected_res = expected_res+str(local_count)+'. '+ 'The bot/user should be able to'+' '+text +'.'+'\n'
                elif 'NOUN' in part_of_speech_1:
                    expected_res = expected_res+str(local_count)+'. '+(extract_information(part_of_speech_1,input_string,output,count))+'.'+'\n'
                else:
                    expected_res = expected_res+ str(local_count) + '. ' + text +'.'+'\n'
                local_count = local_count+1

            with open('Output_Expected_Results.csv', mode='a') as csv_file:               #Opening the file in append mode, so that it does not over-write each entry
                fieldnames = [FieldNameSLNo,FieldNameExpectedResult]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
                writer.writerow({FieldNameSLNo:count,FieldNameExpectedResult: expected_res})
            '''print(expected_res)
            print('\n')'''

    with open('Output_Expected_Results.csv', mode='a') as csv_file:               #Opening the file in append mode, so that it does not over-write each entry
        fieldnames = [FieldNameSLNo,FieldNameExpectedResult]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
        writer.writerow({FieldNameSLNo:count+1,FieldNameExpectedResult: "Bot Closes All The Applications"})

    #print("Run successful...")

if __name__ == "__main__":
    main()