'''
    File name: test_algo.py
    Author: Indrani Chakraborty/Geerisha Jain
    Date created: 02/03/2021
    Date last modified: 21/05/2021
    Python Version: 3.6.8
    Description: It has the algorithm/Code for implementing test cases
'''
import spacy
import string
from csv import DictReader
import csv
import re
from nltk.tokenize import sent_tokenize

count=1
FieldNameSLNo = "SLNo"
FieldNameStep = "Step"
FieldNameTestCase = "Test Case"

with open("Output_TestCase.csv", mode='w') as csv_file:
   fieldnames = [FieldNameSLNo,FieldNameTestCase]
   writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n') 
   writer.writeheader()
   writer.writerow({FieldNameSLNo:'1',FieldNameTestCase: "Download Config File From Sharepoint And Read All The Data's"})

with open('Dataset_TestCase.csv', 'r') as read_obj:                                   
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        count+=1                                                                    
        raw_text= row[FieldNameStep].strip()
        l= list(filter(None, raw_text.split('\n')))
        sentence_break= str(l[0])
        raw_text_list = sent_tokenize(sentence_break)
        text = (raw_text_list[0]).split(':')[0]
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        text = string.capwords(text)
        part_of_speech=[]
        output_text=''
        conjuction = 'CCONJ'

        interogatory_words=['How','When','What']
        special_words=['Appears','Pop-up','Popup','Pops']
        conditional_words=['If','After']
        preposition_words=['Under','In','On']
        article_words=['The','An','A']
        auxiliary_words=['Will', 'Should Be', 'This', 'That']

        if str(bool([i for i in auxiliary_words if(i in text)]))=='True':
            text = text.replace("Will","Should")
            text = text.replace("This","The")
            text = text.replace("That","The")
            text = text.replace("Should Be","Is")

        input_string= text.split(" ")

        for token in doc:
            part_of_speech.append(token.pos_)

        if 'PUNCT' in part_of_speech:
            part_of_speech.remove('PUNCT')
        
        if str(list(filter(text.startswith, interogatory_words)) != [])=='True':
            if 'Bot' in text:
                index_bot=text.split('Bot')
                output_text="Verify If The Bot/User Will "+str(index_bot[1])
                index_bot=[]
            else:
                output_text="Verify "+text

        elif str(bool([i for i in special_words if(i in text)]))=='True':
            if 'Appears' in text:
                index_appear = text.split('Appears')
                output_text="Verify If The User/Bot Is Able To View "+str(index_appear[0])
                index_appear=[]
            else:
                output_text="Verify If The User/Bot Is Able to View The Pop-Up"

        elif str(list(filter(text.startswith, conditional_words)) != [])=='True':
            if ',' in text:
                index_comma = text.split(',')
                if 'Bot' in text:
                    output_text=str(index_comma[0])+", Verify if "+str(index_comma[1])
                else:
                    output_text=str(index_comma[0])+", Verify if the Bot/User is able to "+str(index_comma[1])
                index_comma=[]
            else:
                if 'Else' in text:
                    index_else = text.split('Else')
                    if 'Bot' in text:
                        output_text=str(index_else[0])+", Verify if "+str(index_else[1])
                    else:
                        output_text=str(index_else[0])+", Verify if the Bot/User is able to "+str(index_else[1])
                    index_else=[]
                elif 'Then' in text:
                    index_then = text.split('Then')
                    if 'Bot' in text:
                        output_text=str(index_then[0])+", Verify If "+str(index_then[1])
                    else:
                        output_text="Verify "+str(index_then[0])+"And Perform Necessary Actions"
                    index_then=[]
                else:
                    output_text=text

        elif str(list(filter(text.startswith, preposition_words)) != [])=='True':
            if ',' in text:
                index_comma = text.split(',')
                if text.startswith('Under'):
                    if 'Bot' in text:
                        output_text=str(index_comma[1])+", Verify if "+str(index_comma[0])
                    else:
                        output_text=str(index_comma[1])+", Verify if the Bot/User is able to "+str(index_comma[0])
                else:
                    if 'Bot' in text:
                        output_text= "Verify If "+str(index_comma[1])+" "+str(index_comma[0])
                    else:
                        output_text="Verify If The Bot/User Is Able To "+str(index_comma[1])+" "+str(index_comma[0])
            else:
                if 'Bot' in text:
                    output_text="Verify If "+text
                else:
                    output_text=text

        elif str(list(filter(text.startswith, article_words)) != [])=='True':
            output_text="verify If "+text

        elif conjuction in part_of_speech:
            index_comma = text.split('And')
            if 'Bot' in text:
                index_bot = text.split('Bot')
                output_text="Verify If Bot/User Is Able "+str(index_bot[1])
                index_bot=[]
            else:
                output_text="Verify if the user/Bot is able to "+str(index_comma[0])

        else:
            index=0
            part_word=''
            try:
                if 'PART' in part_of_speech:
                    index = part_of_speech.index('PART')
                    part_word = text.split(' ')[index]
                    new_text=''
                    for j in range(index+1, len(input_string)):
                        new_text=new_text+input_string[j]+" "
                        if 'Bot' in new_text:
                            output_text="Verify if "+new_text
                        else:
                            output_text="Verify if the user/Bot is able to "+new_text
            
                    
                elif 'ADP' in part_of_speech:
                    element = 'ADP'
                    first_index = part_of_speech.index(element)
                    part_of_speech.reverse()
                    last_index = len(part_of_speech)- part_of_speech.index(element)-1
                    if first_index==last_index:
                        if first_index==1:
                            #print(text)
                            if 'Bot' in text:
                                output_text="Verify if  "+text
                            else:
                                output_text="Verify if the bot/User is able to "+text

                        else:
                            new_text=' '
                            condition=0
                            for j in range(0, first_index):
                                part_of_speech.reverse()
                                if (part_of_speech[first_index-1] == "VERB"):
                                    ind = part_of_speech.index('VERB')
                                    res=''
                                    if (input_string[ind].endswith('s')):
                                        input_string[ind] = input_string[ind][:-1]
                                        for z in range(0, first_index-1):
                                            res = res + input_string[z] +" "
                                        new_text = res + "should " + input_string[ind] + " " + input_string[first_index]
                                        condition=1
                                        #print(res + "should " + input_string[ind] + " " + input_string[first_index])
                                    elif (input_string[ind].endswith('ing')):
                                        input_string[ind] = input_string[ind][:-3]
                                        for z in range(0, first_index-2):
                                            res = res + input_string[z] +" "
                                        #print(res + "should " + input_string[ind] + " " + input_string[first_index])
                                        new_text= res + "should " + input_string[ind] + " " + input_string[first_index]
                                        condition=1
                                    break
                            if(condition==0):
                                for j in range(0,first_index):
                                    new_text=new_text+input_string[j]+" "
                            if 'Bot' in new_text:
                                output_text="Verify if "+new_text
                            else:
                                output_text="Verify if the user/Bot is able to "+new_text
                                    
                    else:
                        if first_index==0:
                            #print(text)
                            if 'Bot' in text:
                                output_text="Verify if "+text
                            else:
                                output_text="Verify if the bot/User is able to "+text

                        else:
                            new_text= ''
                            for j in range(0, first_index):
                                new_text=new_text+input_string[j]+" "
                                #print(input_string[j],end=" ")
                            for j in range(last_index,len(input_string)):
                                new_text=new_text+input_string[j]+" "
                                #print(input_string[j],end=" ")
                            if 'Bot' in new_text:
                                output_text= "Verify if "+new_text
                            else:
                                output_text= "Verify if the bot/User is able to "+new_text

                else:
                    #print(text)
                    if 'Bot' in text:
                        output_text="Verify if "+text
                    else:
                        output_text="Verify if the bot/User is able to "+text
            except:
                output_text=text


        output_text= string.capwords(output_text)
        #print(output_text)
        with open('Output_TestCase.csv', mode='a') as csv_file:               #Opening the file in append mode, so that it does not over-write each entry
            fieldnames = [FieldNameSLNo,FieldNameTestCase]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
            writer.writerow({FieldNameSLNo:count,FieldNameTestCase: output_text})
        output_text=''

with open('Output_TestCase.csv', mode='a') as csv_file:               #Opening the file in append mode, so that it does not over-write each entry
    fieldnames = [FieldNameSLNo,FieldNameTestCase]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
    writer.writerow({FieldNameSLNo:count+1,FieldNameTestCase: "Close All The Open Instances"})

#print("Run successful...")

