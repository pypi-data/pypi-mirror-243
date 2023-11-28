import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
import pkg_resources
import re
import requests
import tarfile
import platform
import os
from ftplib import FTP
import RNA
import networkx as nx
import pandas as pd
import subprocess
from Bio import AlignIO
from Bio import Entrez, SeqIO
Entrez.email = "jseq.info@gmail.com"   
from pymsaviz import MsaViz 
import random
import string
from collections import Counter
import seaborn as sns
pd.options.mode.chained_assignment = None
import warnings
import json

warnings.filterwarnings("ignore")


from seq_tools import *



    

# def load_sequences(n:int(), project:dict(), coding = True, **args):
    
#     transcripts = {'name': [], 'SEQ': [], 'sequence': []}
#     for i in range(1,n+1):
#         check = True
#         check_name = True
#         while (check == True or check_name == True):
#             if str('SEQ' + str(i)) not in args and check == True:
#                 globals()[str('SEQ' + str(i))] = input('Enter sequence ' + str('SEQ'+str(i)) + ': ').replace('\\n', '\n')
#                 globals()[str('SEQ' + str(i))] = ''.join(c.upper() for c in eval(str('SEQ' + str(i))) if c.isalpha())
#             if str('SEQ' + str(i) + '_name') not in args and check_name == True:
#                 globals()[str('SEQ' + str(i) + '_name')] = input('Enter sequence name ' + str('SEQ'+str(i)) + ': ')
#                 globals()[str('SEQ' + str(i) + '_name')] = eval(str('SEQ' + str(i) + '_name')).upper()
                
#             if str('SEQ'+str(i)) in args:
#                 test = args[str('SEQ'+str(i))]
#                 test = [args[str('SEQ'+str(i))][y:y+3] for y in range(0, len(args[str('SEQ'+str(i))]), 3)]
#                 test2 = args[str('SEQ'+str(i))].upper()
#                 test2 = list(test2)
                
                
#                 t2 = check_upac(test2)
                
                
#                 if (len(test) == 0):
#                     print("\nSequence not provided. Sequence length equals 0")
#                     check = True  
#                 elif (len(test[-1]) < 3 and coding == True):
#                     print("\nWrong sequence " + str(i) + ". The condition of three-nucleotide repeats in the coding sequence is not met.")
#                     check = True
#                 elif (t2 == False):
#                     check = True
                    
#                 else:
#                     check = False
#                 if (len(args[str('SEQ' + str(i) + '_name')]) == 0):
#                     print("\nWrong name.  Enter sequence name")
#                     check_name = True
                    
#                 else:
#                     check_name = False
                    
#                 if check_name == False and check == False:
#                     transcripts['name'].append(globals()[str('SEQ' + str(i) + '_name')].upper())
#                     transcripts['SEQ'].append(str('SEQ' + str(i)))
#                     transcripts['sequence'].append(''.join(c.upper() for c in globals()[str('SEQ' + str(i))] if c.isalpha()))
                
                
#             else:
#                 test = globals()[str('SEQ'+str(i))]
#                 test = [globals()[str('SEQ'+str(i))][y:y+3] for y in range(0, len(globals()[str('SEQ'+str(i))]), 3)]
#                 test2 = globals()[str('SEQ'+str(i))].upper()
#                 test2 = list(test2)
                
                    
#                 t2 = check_upac(test2, upac_code = ['A','C','T','G','N','M','R','W','S','Y','K','V','H','D','B','U'])
                
                
#                 if (len(test) == 0):
#                     print("\nSequence not provided. Sequence length equals 0")
#                     check = True  
#                 elif (len(test[-1]) < 3 and coding == True):
#                     print("\nWrong sequence " + str(i) + ". The condition of three-nucleotide repeats in the coding sequence is not met.")
#                     check = True
#                 elif (t2 == False):
#                     check = True
                    
                    
#                 else:
#                     check = False
#                 if (len(globals()[str('SEQ' + str(i) + '_name')]) == 0):
#                     print("\nWrong name.  Enter sequence name")
#                     check_name = True
                    
#                 else:
#                     check_name = False
                    
#                 if check_name == False and check == False:
#                     transcripts['name'].append(globals()[str('SEQ' + str(i) + '_name')].upper())
#                     transcripts['SEQ'].append(str('SEQ' + str(i)))
#                     transcripts['sequence'].append(''.join(c.upper() for c in globals()[str('SEQ' + str(i))] if c.isalpha()))
#                     del globals()[str('SEQ' + str(i) + '_name')], globals()[str('SEQ' + str(i))]

     
#     transcript_list = []
#     for i in range(1,n+1):
#         transcript_list.append(str('SEQ'+str(i)))
#         transcript_list.append(str('Linker_'+str(i)))
    
#     transcript_list = transcript_list[0:len(transcript_list) - 1]
#     project['transcripts']['sequences'] = transcripts
#     project['elements']['transcripts'] = transcript_list
    
#     return project  
                


# def select_linkers(n:int(), linkers:pd.DataFrame(), project:dict(), **args):
#     if n < 1:
#         project['elements']['linkers']['linker_1'] = ''
#         project['elements']['linkers']['linker_1_name'] = ''
#     if 'linker_1' not in args and  'linker_1_name' not in args and n > 1:
#         print('-------------------------------------------------------------')
#         print('id : 0')
#         print('Lack of linker between proteins')
#         for lin in linkers['id']:
#             print('-------------------------------------------------------------')
#             print('id : ' + str(lin))
#             print('name : ' + str(linkers['name'][linkers['id'] == lin][lin-1]))
#             print('description : ' + str(linkers['description'][linkers['id'] == lin][lin-1]))
#             print('role : ' + str(linkers['role'][linkers['id'] == lin][lin-1]))
     
    
#         for i in range(1,n):
#             if str('linker_' + str(i)) not in args:
#                 check = True
#                 while (check == True):
#                     locals()['x'] = input('\n Enter id for linker between transcripts ' + str(i) +' & ' + str(int(i+1)) + ': ')
#                     if (len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(linkers['role'])+1)):
#                         if locals()['x'] == str(0):
#                             project['elements']['linkers'][str('linker_'+str(i))] = ''
#                             project['elements']['linkers'][str('linker_'+str(i) + '_name')] = ''
#                         else:
#                             project['elements']['linkers'][str('linker_'+str(i))] = str(linkers['seq'][linkers['id'] == int(locals()['x'])][int(locals()['x'])-1])
#                             project['elements']['linkers'][str('linker_'+str(i) + '_name')] = str(linkers['name'][linkers['id'] == int(locals()['x'])][int(locals()['x'])-1])
    
    
#                         check = False
         
#     elif 'linker_1' in args and  'linker_1_name' in args and n > 1:
#         for key, value in args.items():
#             if 'name' in str(key):
#                 project['elements']['linkers'][str(key)] = str(value)
#             else:
#                 project['elements']['linkers'][str(key)] = str(value)

        
#     return project




# def select_promoter_transkrypts(promoters:pd.DataFrame(), project:dict(), **args):
#     if 'promoter' not in args and 'promoter_name' not in args:
#         for lin in promoters['id']:
#             print('-------------------------------------------------------------')
#             print('id : ' + str(lin))
#             print('name : ' + str(promoters['name'][promoters['id'] == lin][lin-1]))
#             print('specificity : ' + str(promoters['tissue'][promoters['id'] == lin][lin-1]))
#             print('description : ' + str(promoters['description'][promoters['id'] == lin][lin-1]))
#             print('role : ' + str(promoters['role'][promoters['id'] == lin][lin-1]))
#             print('reference : ' + str(promoters['ref'][promoters['id'] == lin][lin-1]))
       
#         check = True
#         while (check == True):
#             x = input('\nEnter id for promoter: ')
#             if (locals()['x'] != '' and int(locals()['x']) > 0 and len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(promoters['role'])+1)):
#                 if x == str(0):
#                     project['elements']['promoter']['sequence'] = ''
#                     project['elements']['promoter']['name'] = ''
#                 else:
#                     project['elements']['promoter']['sequence'] = str(promoters['seq'][promoters['id'] == eval(x)][eval(x)-1])
#                     project['elements']['promoter']['name'] = str(promoters['name'][promoters['id'] == eval(x)][eval(x)-1])

#                 check = False
#     else:
#         project['elements']['promoter']['sequence'] = args['promoter']
#         project['elements']['promoter']['name'] = args['promoter_name']
        
#     return project



# def select_regulator(regulators:pd.DataFrame(), project:dict(), **args):
#     if 'enhancer' not in args and 'enhancer_name' not in args:
#         print('-------------------------------------------------------------')
#         print('id : 0')
#         print('Lack of regulators')
#         for lin in regulators['id']:
#             print('-------------------------------------------------------------')
#             print('id : ' + str(lin))
#             print('name : ' + str(regulators['name'][regulators['id'] == lin][lin-1]))
#             print('description : ' + str(regulators['description'][regulators['id'] == lin][lin-1]))
#             print('role : ' + str(regulators['role'][regulators['id'] == lin][lin-1]))
#             print('type : ' + str(regulators['type'][regulators['id'] == lin][lin-1]))
#             print('reference : ' + str(regulators['ref'][regulators['id'] == lin][lin-1]))
       
#         check = True
#         while (check == True):
#             x = input('\nEnter id for regulator: ')
#             if (len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(regulators['role'])+1)):
#                 if x == str(0):
#                     project['elements']['regulators']['enhancer'] = ''
#                     project['elements']['regulators']['enhancer_name'] = ''

#                 else:
#                     project['elements']['regulators']['enhancer'] = str(regulators['seq'][regulators['id'] == eval(x)][eval(x)-1]) 
#                     project['elements']['regulators']['enhancer_name'] = str(regulators['name'][regulators['id'] == eval(x)][eval(x)-1])
                
#                 check = False
                
#     elif 'enhancer' in args and 'enhancer_name' in args:
#         project['elements']['regulators']['enhancer'] = args['enhancer']
#         project['elements']['regulators']['enhancer_name'] = args['enhancer_name']
        
#     return project
     



# def select_polyA_seq_transkrypts(polya_seq:pd.DataFrame(), project:dict(), **args):
#     if 'polya' not in args and 'polya_name' not in args:
#         print('-------------------------------------------------------------')
#         print('id : 0')
#         print('Default regulator for vector')
#         for lin in polya_seq['id']:
#             print('-------------------------------------------------------------')
#             print('id : ' + str(lin))
#             print('name : ' + str(polya_seq['name'][polya_seq['id'] == lin][lin-1]))
#             print('description : ' + str(polya_seq['description'][polya_seq['id'] == lin][lin-1]))

       
#         check = True
#         while (check == True):
#             x = input('\nEnter id for regulator: ')
#             if (len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(polya_seq['name'])+1)):
#                 if x == str(0):
#                     project['elements']['pol']['polya'] = ''
#                     project['elements']['regulators']['polya_name'] = ''

#                 else:
#                     project['elements']['regulators']['polya'] = str(polya_seq['seq'][polya_seq['id'] == eval(x)][eval(x)-1]) 
#                     project['elements']['regulators']['polya_name'] = str(polya_seq['name'][polya_seq['id'] == eval(x)][eval(x)-1])
                
#                 check = False
                
#     elif 'polya' in args and 'polya_name' in args:
#         project['elements']['regulators']['polya'] = args['polya']
#         project['elements']['regulators']['polya_name'] = args['polya_name']
        
#     return project





# def select_fluorescent_tag(fluorescent_tag:pd.DataFrame(), project:dict(), **args):
#     if 'fluorescence' not in args and 'fluorescence_name' not in args:
#         check_f = True
#         while(check_f == True):
#             if 'fluorescence' not in args and 'fluorescence_name' not in args and check_f == True:
#                 print('-------------------------------------------------------------')
#                 print('id : 0')
#                 print('Lack of fluorescent tag')
#                 for lin in fluorescent_tag['id']:
#                     print('-------------------------------------------------------------')
#                     print('id : ' + str(lin))
#                     print('name : ' + str(fluorescent_tag['name'][fluorescent_tag['id'] == lin][lin-1]))
#                     print('description : ' + str(fluorescent_tag['description'][fluorescent_tag['id'] == lin][lin-1]))
#                     print('role : ' + str(fluorescent_tag['role'][fluorescent_tag['id'] == lin][lin-1]))
#                     print('reference : ' + str(fluorescent_tag['ref'][fluorescent_tag['id'] == lin][lin-1]))
        
#                 locals()['x'] = input('\nEnter id for fluorescent tag: ')
#                 if (len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(fluorescent_tag['role'])+1) ):
#                     check_f = False
#                     if locals()['x'] == str(0):
#                         project['elements']['fluorescence']['sequence'] = ''
#                         project['elements']['fluorescence']['name'] = ''
#                         project['elements']['fluorescence']['linker'] = ''
#                         project['elements']['fluorescence']['linker_name'] = ''
    
#                     else:
#                         project['elements']['fluorescence']['sequence'] = str(fluorescent_tag['seq'][fluorescent_tag['id'] == int(locals()['x'])][int(locals()['x'])-1])
#                         project['elements']['fluorescence']['name'] = str(fluorescent_tag['name'][fluorescent_tag['id'] == int(locals()['x'])][int(locals()['x'])-1])
    
#             if 'fluorescence' in args:
#                 check_f = False
                
               
                    
     
#     else:
#         project['elements']['fluorescence']['sequence'] = args['fluorescence']
#         project['elements']['fluorescence']['name'] = args['fluorescence_name']

        
#     return project


# def select_fluorescent_tag_linker(linkers:pd.DataFrame(), project:dict(), **args):
#     if 'fluorescent_tag_linker' not in args and 'fluorescent_tag_linker_name' not in args:
#         check_l = True
#         while(check_l == True):

#             if 'fluorescent_tag_linker' not in args and 'fluorescent_tag_linker_name' not in args:
#                 print('-------------------------------------------------------------')
#                 print('id : 0')
#                 print('Lack of the linker between the last protein and the fluorescent tag')
#                 for lin in linkers['id']:
#                     print('-------------------------------------------------------------')
#                     print('id : ' + str(lin))
#                     print('name : ' + str(linkers['name'][linkers['id'] == lin][lin-1]))
#                     print('description : ' + str(linkers['description'][linkers['id'] == lin][lin-1]))
#                     print('role : ' + str(linkers['role'][linkers['id'] == lin][lin-1]))
                    
                
#                 locals()['l'] = input('\nEnter id for linker: ')
                
#                 if (len(locals()['l']) > 0) and locals()['l'].isnumeric() and (int(locals()['l']) in range(0, len(linkers['role'])+1)):
#                     check_l = False
#                     if locals()['l'] == str(0):
#                         project['elements']['fluorescence']['linker'] = ''
#                         project['elements']['fluorescence']['linker_name'] = ''
    
#                     else:
#                         project['elements']['fluorescence']['linker'] = str(linkers['seq'][linkers['id'] == int(locals()['l'])][int(locals()['l'])-1])
#                         project['elements']['fluorescence']['linker_name'] = str(linkers['name'][linkers['id'] == int(locals()['l'])][int(locals()['l'])-1])
    
    

     
#     else:
#         project['elements']['fluorescence']['linker'] = args['fluorescent_tag_linker']
#         project['elements']['fluorescence']['linker_name'] = args['fluorescent_tag_linker_name']
        
#     return project




# def select_promoter_tag(promoters:pd.DataFrame(), project:dict(), **args):
#     if 'promoter_tag' not in args and 'promoter_tag_name' not in args:
#         for lin in promoters['id']:
#             print('-------------------------------------------------------------')
#             print('id : ' + str(lin))
#             print('name : ' + str(promoters['name'][promoters['id'] == lin][lin-1]))
#             print('specificity : ' + str(promoters['tissue'][promoters['id'] == lin][lin-1]))
#             print('description : ' + str(promoters['description'][promoters['id'] == lin][lin-1]))
#             print('role : ' + str(promoters['role'][promoters['id'] == lin][lin-1]))
#             print('reference : ' + str(promoters['ref'][promoters['id'] == lin][lin-1]))
       
#         check = True
#         while (check == True):
#             x = input('\nEnter id for promoter: ')
#             if (locals()['x'] != '' and int(locals()['x']) > 0 and len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(promoters['role'])+1)):
#                 if x == str(0):
#                     project['elements']['fluorescence']['promoter_seq'] = ''
#                     project['elements']['fluorescence']['promoter_name'] = ''
#                 else:
#                     project['elements']['fluorescence']['promoter_seq'] = str(promoters['seq'][promoters['id'] == eval(x)][eval(x)-1])
#                     project['elements']['fluorescence']['promoter_name'] = str(promoters['name'][promoters['id'] == eval(x)][eval(x)-1])

#                 check = False
#     else:
#         project['elements']['fluorescence']['promoter_seq'] = args['promoter_tag']
#         project['elements']['fluorescence']['promoter_name'] = args['promoter_tag_name']
        
#     return project




# def select_polyA_seq_tag(polya_seq:pd.DataFrame(), project:dict(), **args):
#     if 'polya_seq_tag' not in args and 'polya_seq_tag_name' not in args:
#         print('-------------------------------------------------------------')
#         print('id : 0')
#         print('Default regulator for vector')
#         for lin in polya_seq['id']:
#             print('-------------------------------------------------------------')
#             print('id : ' + str(lin))
#             print('name : ' + str(polya_seq['name'][polya_seq['id'] == lin][lin-1]))
#             print('description : ' + str(polya_seq['description'][polya_seq['id'] == lin][lin-1]))

       
#         check = True
#         while (check == True):
#             x = input('\nEnter id for regulator: ')
#             if (len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(polya_seq['name'])+1)):
#                 if x == str(0):
#                     project['elements']['fluorescence']['polya_seq'] = ''
#                     project['elements']['fluorescence']['polya_seq_name'] = ''

#                 else:
#                     project['elements']['fluorescence']['polya_seq'] = str(polya_seq['seq'][polya_seq['id'] == eval(x)][eval(x)-1]) 
#                     project['elements']['fluorescence']['polya_seq_name'] = str(polya_seq['name'][polya_seq['id'] == eval(x)][eval(x)-1])
                
#                 check = False
                
#     elif 'polya_seq_tag' in args and 'polya_seq_tag_name' in args:
#         project['elements']['fluorescence']['polya_seq'] = args['polya_seq_tag']
#         project['elements']['fluorescence']['polya_seq_name'] = args['polya_seq_tag_name']
        
#     return project




# def select_selection_marker(selection_marker:pd.DataFrame(), project:dict(), **args):
#     if 'selection_marker' not in args and 'selection_marker_name' not in args:
#         print('-------------------------------------------------------------')
#         print('id : 0')
#         print('Default regulator for vector')
#         for lin in selection_marker['id']:
#             print('-------------------------------------------------------------')
#             print('id : ' + str(lin))
#             print('name : ' + str(selection_marker['name'][selection_marker['id'] == lin][lin-1]))
#             print('description : ' + str(selection_marker['description'][selection_marker['id'] == lin][lin-1]))

       
#         check = True
#         while (check == True):
#             x = input('\nEnter id for regulator: ')
#             if (len(locals()['x']) > 0) and locals()['x'].isnumeric() and (int(locals()['x']) in range(0, len(selection_marker['name'])+1)):
#                 if x == str(0):
#                     project['elements']['vector']['selection_marker'] = ''
#                     project['elements']['vector']['selection_marker_name'] = ''

#                 else:
#                     project['elements']['vector']['selection_marker'] = str(selection_marker['seq'][selection_marker['id'] == eval(x)][eval(x)-1]) 
#                     project['elements']['vector']['selection_marker_name'] = str(selection_marker['name'][selection_marker['id'] == eval(x)][eval(x)-1])
                
#                 check = False
                
#     elif 'selection_marker' in args and 'selection_marker_name' in args:
#         project['elements']['vector']['selection_marker'] = args['selection_marker']
#         project['elements']['vector']['selection_marker_name'] = args['selection_marker_name']
        
#     return project






# def create_vector(metadata):
#     import re
#     while (True):
        
#             project_name = input('Enter project name [min 3 & max 20 letters]: ')
#             if project_name and len(project_name) > 20:
#                 print('The name is too long...')
#             elif project_name and len(project_name) < 3:
#                 print('The name is too short...')
#             elif project_name and len(project_name) >= 3 & len(project_name) <= 20:
#                 project_name = str(re.sub(r'\s+', '_', project_name))
#                 break
#     while (True):
#             df = pd.DataFrame({'id':list(range(0,len(set(metadata['vectors']['vector_type'])))),
#                   'name': sorted(list(set(metadata['vectors']['vector_type'])), reverse = True)})
            
#             print('Select vector type:')
#             print('id : name')
#             for i in df['id']: 
#                 print('-------------------------------------------------------------')
#                 print(str(i) + ' : ' + str(df['name'][df['id'] == i][df['name'][df['id'] == i].index[0]]))
#                 print('-------------------------------------------------------------')
           

#             dec = input('Enter vector type id: ')
#             if dec and int(dec) in list(df['id']):
#                 vector_type = str(df['name'][df['id'] == int(dec)][df['name'][df['id'] == int(dec)].index[0]])
#                 break
#             else:
#                 print('Provided wrong id...')
                
#     while (True):
#             df = pd.DataFrame({'id':list(range(0,len(set(metadata['vectors']['function'])))),
#                   'name': sorted(list(set(metadata['vectors']['function'])), reverse = True)})
            
#             print('Select vector function:')
#             print('id : name')
#             for i in df['id']: 
#                 print('-------------------------------------------------------------')
#                 print(str(i) + ' : ' + str(df['name'][df['id'] == i][df['name'][df['id'] == i].index[0]]))
#                 print('-------------------------------------------------------------')
           

#             dec = input('Enter vector type id: ')
#             if dec and int(dec) in list(df['id']):
#                 vector_function = str(df['name'][df['id'] == int(dec)][df['name'][df['id'] == int(dec)].index[0]])
#                 break
#             else:
#                 print('Provided wrong id...')
                
#     while (True):
#             df = pd.DataFrame({'id':list(range(0,len(set(metadata['codons']['Species'])))),
#                   'name': sorted(list(set(metadata['codons']['Species'])), reverse = True)})
            
#             print('Select species:')
#             print('id : name')
#             for i in df['id']: 
#                 print('-------------------------------------------------------------')
#                 print(str(i) + ' : ' + str(df['name'][df['id'] == i][df['name'][df['id'] == i].index[0]]))
#                 print('-------------------------------------------------------------')
           

#             dec = input('Enter speciers id: ')
#             if dec and int(dec) in list(df['id']):
#                 species = str(df['name'][df['id'] == int(dec)][df['name'][df['id'] == int(dec)].index[0]])
#                 break
#             else:
#                 print('Provided wrong id...')
                
#     project = create_project(project_name)
    
#     while (True):
           
#             print('Indicate how many transcripts you want to insert into the vector, not counting the fluorescent tag. [min 1 / max 4]:')
#             print('')
#             n = int(input('Enter the number of transcripts: '))
#             if n and int(n) in [1,2,3,4]:
#                 break
#             else:
#                 print('')
#                 print('Provided wrong number of transcripts...')
        
  
    
#     try:
#         project = load_sequences(n, project, coding = True)
#     except:
#         print('\nSomething went wrong with sequence loading...')
        
#     try:
#         project = select_linkers(n, metadata['linkers'], project)
#     except:
#         print('\nSomething went wrong with linkers selection...')
        
#     try:
#         project = select_promoter_transkrypts(metadata['promoters'], project)
#     except:
#         print('\nSomething went wrong with promoter selection...')
#     project = select_regulator(metadata['regulators'], project)
    
#     try:
#         project = select_polyA_seq_transkrypts(metadata['polya_seq'], project)
#     except:
#         print('\nSomething went wrong with polyA sequence selection...')
       
#     try:
#         project = select_fluorescent_tag(metadata['fluorescent_tag'], project)
#     except:
#         print('\nSomething went wrong with fluorescent tag selection...')
    
#     if len(project['elements']['fluorescence']['sequence']) > 0:
        
#         while (True):
#                 df = pd.DataFrame({'id':list(range(0,len(set(metadata['backbone']['promoter'])))),
#                       'format': sorted(list(set(metadata['backbone']['promoter'])), reverse = True)})
                
#                 print('Do you want to use separate promoters for fluorescent tag and transcripts?')
#                 print('single - one promoter for both, multiple - different promoters')
#                 print('id : format')
#                 for i in df['id']: 
#                     print('-------------------------------------------------------------')
#                     print(str(i) + ' : ' + str(df['format'][df['id'] == i][df['format'][df['id'] == i].index[0]]))
#                     print('-------------------------------------------------------------')
               

#                 dec = input('Enter decision: ')
#                 if dec and int(dec) in list(df['id']):
#                     promoter_dec = str(df['format'][df['id'] == int(dec)][df['format'][df['id'] == int(dec)].index[0]])
#                     break
#                 else:
#                     print('Provided wrong id...')
        
#         try:
#             if promoter_dec == 'single':
#                 project = select_fluorescent_tag_linker(metadata['linkers'], project)
#                 project = select_promoter_tag(metadata['promoters'], project, promoter_tag = '', promoter_tag_name = '')
#                 project = select_polyA_seq_tag(metadata['polya_seq'], project, polya_seq_tag = '', polya_seq_tag_name = '') 
#             else:
#                 project = select_promoter_tag(metadata['promoters'], project)
#                 project = select_polyA_seq_tag(metadata['polya_seq'], project) 
#                 project = select_fluorescent_tag_linker(metadata['linkers'], project, fluorescent_tag_linker = '', fluorescent_tag_linker_name = '')
        
#         except:
#             print('\nSomething went wrong with promoters selection...')
            
            
#     else:
#         try:
#             project = select_fluorescent_tag_linker(metadata['linkers'], project, fluorescent_tag_linker = '', fluorescent_tag_linker_name = '')
#             project = select_promoter_tag(metadata['promoters'], project, promoter_tag = '', promoter_tag_name = '')
#             project = select_polyA_seq_tag(metadata['polya_seq'], project, polya_seq_tag = '', polya_seq_tag_name = '') 
#         except:
#             print('\nSomething went wrong with promoters selection...')
    
#     try:
#         project = select_selection_marker(metadata['selection_markers'], project)
#     except:
#         print('\nSomething went wrong with selection marker selection...')
        
#     #poprawic stop check
#     try:
#         project = check_stop(project, metadata['codons'], promoter_dec)
        
#     except:
#         print('\nSomething went wrong with codon stop establishment...')
    
#     while (True):
#             df = pd.DataFrame({'id':list(range(0,2)),
#                   'decision': ['no', 'yes'],
#                   'tf': [False, True]})
            
#             print('Do you want to enrich your coding sequences for better protein expression?')
#             print('no / yes')
#             print('id : format')
#             for i in df['id']: 
#                 print('-------------------------------------------------------------')
#                 print(str(i) + ' : ' + str(df['decision'][df['id'] == i][df['decision'][df['id'] == i].index[0]]))
#                 print('-------------------------------------------------------------')
           

#             dec = input('Enter decision: ')
#             if dec and int(dec) in list(df['id']):
#                 run1 = bool(df['tf'][df['id'] == int(dec)][df['tf'][df['id'] == int(dec)].index[0]])
#                 break
#             else:
#                 print('Provided wrong id...')
                
#     try:
#         project = sequence_enrichment(project, metadata['codons'], species, run = run1)
#     except:
#         print('\nSomething went wrong with sequence enrichment...')
        
#     if run1 == True:
#         project = select_sequence_variant(project)
     
#     while (True):
#             df = pd.DataFrame({'id':list(range(0,2)),
#                   'decision': ['no', 'yes'],
#                   'tf': [False, True]})
            
#             print('Do you want to check your coding sequences for existing restriction places?')
#             print('no / yes')
#             print('id : format')
#             for i in df['id']: 
#                 print('-------------------------------------------------------------')
#                 print(str(i) + ' : ' + str(df['decision'][df['id'] == i][df['decision'][df['id'] == i].index[0]]))
#                 print('-------------------------------------------------------------')
           

#             dec = input('Enter decision: ')
#             if dec and int(dec) in list(df['id']):
#                 run2 = bool(df['tf'][df['id'] == int(dec)][df['tf'][df['id'] == int(dec)].index[0]])
#                 break
#             else:
#                 print('Provided wrong id...')
#     try:             
#         project = find_restriction_vector(project, metadata['restriction'], run = run2)
        
#         if run2 == True:
#             project = remove_restriction_vector(project, metadata['restriction'])
#             project = repair_restriction_vector(project, metadata['restriction'], metadata['codons'], species)
            
#     except:
#         print('\nSomething went wrong with restriction places remove...')
        
    
#     try:
#         project = vector_string(project, metadata['backbone'], vector_type, vector_function, promoter_dec)
#     except:
#         print('\nSomething went wrong with vector building...')
        
#     try:
#         project = eval_vector(project, metadata['vectors'], vector_type, vector_function)
#     except:
#         print('\nSomething went wrong with vector evaluation...')
        
        
#     try:
#         project, pl = vector_plot_project(project, metadata)
#     except:
#         print('\nSomething went wrong with vector ploting...')

#     return project




