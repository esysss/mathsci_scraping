import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas

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
        data = data[1]
        try:
            data['Name'] = name[0]
        except:
            data['Name'] = str(linkCounter)

        df = pandas.concat([df, data])
    else:
        problemedLinks.append((url, name[0]))

driver.close()

# check for problemed links, maybe the problem was your internet connection
driver = webdriver.Chrome()
realProblems = []
for linkk in problemedLinks:
    url = linkk[0]
    name = linkk[1]
    data = getTable(url)
    if data[0]:
        data = data[1]
        data['Name'] = name
        df = pandas.concat([df, data])
    else:
        realProblems.append((url, name))

df = df[['Name', 'Year', 'MCQ', 'Cit.(5yr)', 'Pub.(5yr)']]
df.set_index('Name')

#now export it:
export_csv = df.to_csv(r'C:\Users\Esysss\OneDrive\Programming\Web Scrapping Using python\Data.csv', header=True)

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
    except:
        return [False]
    for pd in pds:
        if 'MCQ' in pd:
            return (True,pd)
    return [False]
