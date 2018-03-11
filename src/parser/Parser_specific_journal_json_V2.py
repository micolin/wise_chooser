# Parser for specific journals

import os
from bs4 import BeautifulSoup
import json
import datetime

# save log but does not work at all hahaha
log_name = 'Log/Paser_specific_journal_json' + str(datetime.datetime.now()) + '.txt'
log = open(log_name, 'w')

# journal counter for statistics
journal_counter = 0

# create an empty dictionary
j_dict = {}

# parse the html file
path = '/Users/Kai/PycharmProjects/Config_parser/Raw_html'
dirs = os.listdir(path)
html_counter = 0
total_html = len(dirs)

for html in dirs:
    if html.endswith('.html'):
        html_counter = html_counter + 1
        print >> log, str(html_counter) + '/' + str(total_html)
        print >> log, 'file name ' + html
        print str(html_counter) + '/' + str(total_html)
        print 'file name ' + html


        fp = open(path+'/'+html)
        soup = BeautifulSoup(fp, 'html5lib')
        table = soup.find_all('tbody')
        journal_table = table[3].find_all('tr')  # 4th table is the table wanted; abbr. as jt

        jt_length = len(journal_table)
        if jt_length > 3:
            for i in range(2, jt_length-1):
                journal_counter = journal_counter + 1
                print >> log, 'journal counter: ' + str(journal_counter)
                print 'journal counter: ' + str(journal_counter)
                # parse the table for specific journals
                j = journal_table[i].find_all('td')  # all data entry in one journal; abbr. as j
                j_dict = {}
                if len(j) == 12:
                    j_name = j[1].get_text()
                    j_dict[j_name] = {}
                    j_dict[j_name]['ISSN'] = j[0].get_text()
                    j_dict[j_name]['Impact factor'] = j[2].get_text()
                    j_dict[j_name]['Level'] = j[3].get_text()
                    j_dict[j_name]['Category'] = j[4].get_text()
                    j_dict[j_name]['Sub-category'] = j[5].get_text()
                    if len(j[6].get_text()) == 7:  # SCI must be SCIE
                        j_dict[j_name]['SCI'] = 'Yes'
                        j_dict[j_name]['SCIE'] = 'Yes'
                    elif len(j[6].get_text()) == 4:
                        j_dict[j_name]['SCI'] = 'No'
                        j_dict[j_name]['SCIE'] = 'Yes'
                    else:
                        j_dict[j_name]['SCI'] = 'No'
                        j_dict[j_name]['SCIE'] = 'No'
                    j_dict[j_name]['OA status'] = j[7].get_text()
                    j_dict[j_name]['Successful ratio'] = j[8].get_text()
                    j_dict[j_name]['Review time'] = j[9].get_text()
                    recent = j[10].find('a') # Recent papers is a link
                    j_dict[j_name]['Recent papers'] = recent['href']
                    j_dict[j_name]['Viewed count'] = j[11].get_text()
                    # save journal into single json file
                    json_file = json.dumps(j_dict)
                    json_save = open('Journal_data_json/'+str(journal_counter)+'_'+j_name+'.json', 'w')
                    json.dump(json_file, json_save)
                else:
                    print >> log, 'UNCOMPLETED data in this journal'
                    print 'UNCOMPLETED data in this journal'
        else:
            print >> log, 'No journal to be processed'
            print 'No journal to be processed'

# finish process all the html files
# close the log file
log.close()