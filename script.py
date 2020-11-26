import requests
from bs4 import BeautifulSoup
import re
import csv
import urllib.request
import os


datas=[]

arr=['Degree','Career Title','Membership','Skills','Goal','Certification']      #    //for later checks
i=0

cURL="https://www.myvisajobs.com/CV/Candidates.aspx?P="                #    //central browsing URL
dURL="https://www.myvisajobs.com"                                     #   //domain URL
attach=1
hURL=cURL+str(attach)                                                #//home URL for browsing different pages
page=requests.get(hURL)
soup=BeautifulSoup(page.content,'html.parser')
results=soup.find(id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent")      #results found in this div container
if not os.path.exists('./Images'):
    os.mkdir("./Images")
pattern='-CV-\d+\d+\d+'                        #filtering out other results, also all links are of format -CV-1234

while(1):
    for link in soup.find_all('a'):      
        if(re.search(pattern, link.get('href')) and link.find('img')):                     #getting hyperlinks, and checking if image to avoid repitition
            if(i>=10):
                break
            else:
                name=Degree=CareerTitle=Membership=Skills=Goal=Certification="N/A"
                pURL=link.get('href')
                fURL=dURL+pURL;                                                                              #pURL only gives relative, so making fURL (full)
                page=requests.get(fURL)
                soup=BeautifulSoup(page.content,'lxml')
                results=soup.find(id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_divContent")
                i+=1
                Name=results.h3.text
                imgname="./Images/"+str(i)+'.'+Name+'.jfif'                                                  #making a directory to store images
                urllib.request.urlretrieve(dURL+link.find('img').get('src'),imgname)               #getting images and storing by the name
                print(i)
                for tr in results.find_all('tr')[7:28]:                                   #trimming 7-28 to filter out other tr tags, searching by tr tags as no class tags exist
                    td=tr.find_all('td')
                    if (len(td[0].text)<30) and any(x in td[0].text for x in arr):                        #the initial array for checking attributes
                        try:
                            Code= td[0].text[:-2] + "= td[1].text" + '.replace(\"\\n\",\" \")'                   #creating a variable to store current data
                            exec(Code)
                            
                        except:
                            Code="CareerTitle=" + "td[1].text"  + '.replace(\"\\n\",\" \")'                        #as career title had a space, exception
                            exec(Code)

                datas.append([i,Name, Degree, CareerTitle, Skills, Goal, Membership, Certification])                 #appending data


    if(i>=10):
        break
    attach+=1
    hURL=cURL+str(attach)                                                  #after one page is done, going to the next page and looped with while
    page=requests.get(hURL)
    soup=BeautifulSoup(page.content,'html.parser')


with open('output.csv', 'w', newline='') as file:                                                       #writing to the csv file
    writer = csv.writer(file)
    headers = ['No','Name','Degree','CareerTitle', 'Skills','Goal','Membership','Certification']
    writer.writerow(headers)
    for data in datas:
        writer.writerow(data)


    