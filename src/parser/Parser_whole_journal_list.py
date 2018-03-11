from bs4 import BeautifulSoup
import requests
import pandas as pd

journal_page = requests.get("http://www.letpub.com.cn/index.php?page=journalapp&fieldtag=all&firstletter=")
#print(journal_page.content)
soup = BeautifulSoup(journal_page.content, 'html5lib')
#print(soup)
table = soup.find_all(id = 's1')
journal_table = table[0].find_all('a')
journal_http = []
journal_name = []
for i in range(0, len(journal_table)):
    journal_http.append(journal_table[i]['href'])
    journal_name.append(journal_table[i].get_text())

df = pd.DataFrame(data={'Journal name': journal_name, 'Journal link': journal_http})
df.to_csv(path_or_buf='Journal_list.csv', encoding='utf-8_sig')

