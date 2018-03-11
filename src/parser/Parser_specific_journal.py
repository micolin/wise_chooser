# Parser for specific journals

import os
from bs4 import BeautifulSoup
import pandas as pd
import sys
import datetime

# journal counter for statistics
journal_counter = 0

# parsed journal into a excel file
j_issn = []
j_name = []
j_if = []  # impact factor
j_level = []  # level 1-4
j_cat = []  # general category
j_subcat = []  # journal sub-categroy
j_sci = []  # journal sci indexed or not
j_scie = []  # journal scie indexed or not
j_oa = []  # unknown property hahaha
j_ratio = []  # successful ratio
j_rev_time = []  # time for review
j_recent = []  # a link for the recent published paper; not so useful
j_view = []  # number of reads

path = '/Users/Kai/PycharmProjects/Config_parser/Raw_html'
dirs = os.listdir(path)
html_counter = 0
total_html = len(dirs)
for html in dirs:
    if html.endswith('.html'):
        html_counter = html_counter + 1
        print (str(html_counter) + '/' + str(total_html) + ' file name ' + html + '...')

        with open(path+'/'+html) as fp:
            soup = BeautifulSoup(fp, 'html5lib')
            table = soup.find_all('tbody')
            journal_table = table[3].find_all('tr')  # 4th table is the table wanted; abbr. as jt

            jt_length = len(journal_table)
            if jt_length > 3:
                for i in range (2, jt_length-1):
                    journal_counter = journal_counter + 1
                    print ('journal counter: ' + str(journal_counter))
                    # parse the table for specific journals
                    j = journal_table[i].find_all('td')  # all data entry in one journal; abbr. as j
                    if len(j) == 12:
                        j_issn.append(j[0].get_text())
                        j_name.append(j[1].get_text())
                        j_if.append(j[2].get_text())
                        j_level.append(j[3].get_text())
                        j_cat.append(j[4].get_text())
                        j_subcat.append(j[5].get_text())
                        # for the sci and/or scie property
                        if len(j[6].get_text()) == 7:  # SCI must be SCIE
                            j_sci.append('Yes')
                            j_scie.append('Yes')
                        elif len(j[6].get_text()) == 4:
                            j_sci.append('No')
                            j_scie.append('Yes')
                        else:
                            j_sci.append('No')
                            j_scie.append('No')
                        j_oa.append(j[7].get_text())
                        j_ratio.append(j[8].get_text())
                        j_rev_time.append(j[9].get_text())
                        j_recent.append(j[10].get_text())
                        j_view.append(j[11].get_text())
                    else:
                        print ('UNCOMPLETED data in this journal')
            else:
                print ('No journal to be processed')

# finish process all the html files
# save data
df = pd.DataFrame(data={'ISSN':j_issn,
                        'Name':j_name,
                        'Impact factor':j_if,
                        'Level':j_level,
                        'Category':j_cat,
                        'Sub-category':j_subcat,
                        'SCI':j_sci,
                        'SCIE':j_scie,
                        'OA status':j_oa,
                        'Acceptance ratio':j_ratio,
                        'Review time':j_rev_time,
                        'Recent papers link':j_recent,
                        'Viewed count':j_view
                        })
df.to_csv(path_or_buf='Journal_data.csv', encoding='utf-8_sig')
print ('Save data successfully')

# save log but does not work at all hahaha
log_name = 'Log/' + str(datetime.datetime.now()) + '.txt'
log = open(log_name, 'w')
sys.stdout = log
log.close()








