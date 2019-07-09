import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas
import names

# open the website :
urlpage = 'https://mathscinet.ams.org/mathscinet/mrcit/journal_list.html'

html_page = urllib.request.urlopen(urlpage)
soup = BeautifulSoup(html_page)
links = []
# get the links and the name of jurnals
for link in soup.findAll('a'):
    links.append((link.get('href'),link.contents))

driver = webdriver.Chrome()
df = pandas.DataFrame()
problemedLinks = []
for linkCounter in range(15, len(links)):
    url = 'https://mathscinet.ams.org' + links[linkCounter][0]
    name = links[linkCounter][1]
    data = getTable(url)
    if data[0]:
        newdf = data[1]
        try:
            newdf['Name'] = data[2]
        except:
            newdf['Name'] = str(linkCounter)

        df = pandas.concat([df, newdf])
    else:
        problemedLinks.append((url, name[0]))

driver.close()

# check for problemed links
# driver = webdriver.Chrome()
# realProblems = []
# for linkk in problemedLinks:
#     url = linkk[0]
#     name = linkk[1]
#     data = getTable(url)
#     if data[0]:
#         data = data[1]
#         data['Name'] = name
#         df = pandas.concat([df,data])
#     else:
#         realProblems.append((url,name))

df = df[['Name', 'Year', 'MCQ', 'Cit.(5yr)', 'Pub.(5yr)']]
df.set_index('Name')

#we see the names has kind of problems, so we should fix them

outerDataFram = names.fixingNames(df)

#now export it:(you should change the address obviously!!!)
export_csv = outerDataFram.to_csv(r'C:\Users\Esysss\OneDrive\Programming\Web Scrapping Using python\MathSciNetFinal - edition 1\Data.csv', index = None, header=True)



def getTable(urlpage):
    # get web page
    driver.get(urlpage)
    # execute script to scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    # sleep for 5s
    time.sleep(5)

    thePage = driver.find_element_by_xpath("/html/body")
    try:
        pds = pandas.read_html(thePage.get_attribute('innerHTML'))
        name = driver.find_element_by_class_name("text-ams-orange")
        name = name.get_attribute('innerHTML')
    except:
        return [False]
    for pd in pds:
        if 'MCQ' in pd:
            return (True, pd, name)
    return [False]


