'''
    File name: merger.py
    Author: Indrani/Geerisha
    Date created: 10/03/2021
    Date last modified: 05/04/2021
    Python Version: 3.6.8
    Description: Merger script for populating Module, Test Cases and Expected Results in one Test Case Document

'''

import openpyxl                                                             #Importing Packages
from csv import DictReader

workbook = openpyxl.load_workbook('Test Case Template_V1.0.xlsx')           #Final Test case document is loaded
worksheet = workbook.get_sheet_by_name('Test Cases')                        #Multiple sheets are there in Test case document, script to choose 'Test Cases' sheet
count = 34

with open('Output_TestCase.csv', 'r') as read_obj:                          #Reading the Test cases formed                                 
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:                                                                
        raw_text= row['Test Case'].strip()
        cell = ''
        cell = 'D'+str(count)                                               #Column C should be populated with Test Cases
        worksheet[cell]= raw_text
        workbook.save('Test Case Template_V1.0.xlsx')                       #Saving the test case document
        count = count+1

count_1 = 34
with open('Output_module.csv', 'r') as read_obj:                            #Reading the Modules for each step in the design document                                 
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:                                                                  
        raw_text= row['Module'].strip()
        cell_1 = ''
        cell_2 = ''
        cell_1 = 'C'+str(count_1)                                           #Column B should be populated with Module
        cell_2 = 'B'+str(count_1)                                           #Column A should be populated with the Step no.
        worksheet[cell_1]= raw_text
        worksheet[cell_2]= count_1-33
        workbook.save('Test Case Template_V1.0.xlsx')                       #Saving the Test Case Document
        count_1 = count_1+1

count_2=34
with open('Output_Expected_Results.csv', 'r') as read_obj:                  #Reading the Expected Results for each test case                       
    csv_dict_reader = DictReader(read_obj)
    for row in csv_dict_reader:                                                                  
        raw_text= row['Expected Result'].strip()
        cell_3 = ''
        cell_3 = 'E'+str(count_2)                                           #Column D should be populated with Expected Results
        worksheet[cell_3]= raw_text
        workbook.save('Test Case Template_V1.0.xlsx')                       #Saving the Test Case document
        count_2 = count_2+1
        
