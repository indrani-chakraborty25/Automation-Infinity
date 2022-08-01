'''
    File name: module_algo.py
    Author: Indrani Chakraborty
    Date created: 19/02/2021
    Date last modified: 22/02/2021
    Python Version: 3.6.8
    Description: This is the header for module_algo.py. It aims at creating an algorithm for reading the Design Document steps and populating the module.

'''

import re                                                                           #Importing modules
from csv import DictReader
import csv
import string

csvFileName = "Dataset_TestCase.csv"
outPutModule = "Output_module.csv"

'''Application_name= input('Enter the Application Name')                            #This module will be done by Blueprism and then provide an imput to Python
Full_Application_name= Application_name+' '+'Application'
with open('data_module.csv', mode='a') as csv_file:
    fieldnames = ['Word',FieldNameModule]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
    writer.writerow({'Word':Application_name,FieldNameModule: Full_Application_name})
'''
FieldNameSLNo = "SLNo"
FieldNameStep = "Step"
FieldNameModule = "Module"

with open(outPutModule, mode='w') as csv_file:
   fieldnames = [FieldNameSLNo,FieldNameModule]
   writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n') 
   writer.writeheader()
   writer.writerow({FieldNameSLNo:1,FieldNameModule: "Excel"})

reader = csv.reader(open('data_module.csv', 'r'))                                   #Creating a dataset of modules
search_list_dict = {}                                                               #Reads the columns of CSV and converts it into a dictionary
for row in reader:                                                                  #Create a list of tuples in Python
   k, v = row
   search_list_dict[k] = v
dict_list = list(search_list_dict.items())
search_list=[]
for element in dict_list:                                                           #Creating a list of the keys of the dictionary
    search_list.append(element[0])
count=1
previous_module=[]
previous_module_word=''
last_module=[]
with open(csvFileName, 'r',encoding="utf8") as read_obj:                                   #Read the Design Document steps
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:
        count+=1                                                                #To populate the S.No in Test case document
        input_string= row[FieldNameStep].strip()                                           #Process the steps of the design document step by step
        punctuations = '!()[].{};:"\/,<>/?@#$%^&*_~'
        no_punct = ""
        for char in input_string:
           if char not in punctuations:
              no_punct = no_punct + char
        input_string=no_punct 
   
        if re.compile('|'.join(search_list),re.IGNORECASE).search(input_string):    #Check if the sentence has a module name
            #s= input_string.split(" ")                                              #If yes, split all the words for that step
            s = re.findall(r'\w+', input_string)
            current_module=[]
            unique_current_module=[]
            current_module_word=''

            for i in range(0,len(s)):                                               #Check which module is mentioned in the sentence
                word=s[i]
                for j in dict_list:
                    if word.casefold() ==(j[0].casefold()):                         #Find the module and case should not matter
                        current_module.append(j[1])                                 #Appending the words to the current list\
                        previous_module.append(current_module)                      #Appending all the current modules and storing as previous module
            for k in current_module:                                                #Making sure, the same module names are not present in the list
                if not k in unique_current_module:
                    unique_current_module.append(k)
                    unique_current_module.append(',')
            current_module_word=current_module_word.join(unique_current_module)     #Converting the list of modules to string
            current_module_word=current_module_word[0:len(current_module_word)-1]
            if len(current_module)!=0:                                              #If module is written in that step, current module length would never be 0
                #print(current_module_word)
                filename = outPutModule                                     #Creating a Test case document with csv format
                fields = [FieldNameSLNo,FieldNameModule]                                          #This algorithm is built for populating S.No and Module used
                with open(outPutModule, mode='a') as csv_file:               #Opening the file in append mode, so that it does not over-write each entry
                    fieldnames = [FieldNameSLNo,FieldNameModule]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
                    writer.writerow({FieldNameSLNo:count,FieldNameModule: current_module_word})  #Populate the Output sheet with module name, if name is mentioned in the step
            else:
               #print(current_module)
               filename = outPutModule                                      #Creating a Test case document with csv format
               fields = [FieldNameSLNo,FieldNameModule]                                          #This algorithm is built for populating S.No and Module used
               with open(outPutModule, mode='a') as csv_file:               #Opening the file in append mode, so that it does not over-write each entry
                  fieldnames = [FieldNameSLNo,FieldNameModule]
                  writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
                  writer.writerow({FieldNameSLNo:count,FieldNameModule: current_module})  #Populate the Output sheet with module name, if name is mentioned in the step
                    

                
        else:
            unique_previous_module=[]                                               #If the step is in continuation with the previous step
            try:
                last_module=previous_module[len(previous_module)-1]                     #Check for the module in the previous step
            except:
                last_module='Application'
            for p in last_module:                                                   #Make sure the module has unique module names
                if not p in unique_previous_module:
                    unique_previous_module.append(p)
                    unique_previous_module.append(',')
            previous_module_word=previous_module_word.join(unique_previous_module)
            previous_module_word=previous_module_word[0:len(previous_module_word)-1]
            #print(previous_module_word)
            with open(outPutModule, mode='a') as csv_file:                   #Opening the test case document in append mode
                    fieldnames = [FieldNameSLNo,FieldNameModule]
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
                    writer.writerow({FieldNameSLNo:count,FieldNameModule: previous_module_word})  #Populating the output sheet with module name, if the step is continuation of the last step
            previous_module_word=""

with open(outPutModule, mode='a') as csv_file:                   #Opening the test case document in append mode
    fieldnames = [FieldNameSLNo,FieldNameModule]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')
    writer.writerow({FieldNameSLNo:count+1,FieldNameModule: "Generic/All Applications"})

#print("Run Successful...")
