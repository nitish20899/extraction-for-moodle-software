#!/usr/bin/env python
# coding: utf-8

# In[5]:


from requests import Session
from bs4 import BeautifulSoup as bs
import requests
import bs4
import urllib.request
from urllib.request import urlopen as uReq
import re 
import pandas as pd

 
with Session() as s:
    site = s.get("https://moodle.ubishops.ca/login/index.php")
    bs_content = bs(site.content, "html.parser")
    token = bs_content.find("input", {"name":"logintoken"})["value"]
    user_name = input("Enter the username: ")
    password_1 = input("Enter the password: ")
    login_data = {"username":user_name,"password":password_1, "logintoken":token}
    s.post("https://moodle.ubishops.ca/login/index.php",login_data)
    home_page = s.get("https://moodle.ubishops.ca")
    bs_content1 = bs(home_page.content, "html.parser")
    bs_content2 = bs_content1.findAll("nav", {"class": "list-group"})
    first_links=[]
    for beta in bs_content2[0].findAll('a'):
        first_links.append(beta['href'])
    courses=[]
    for link in first_links[4:-1]:
        home_page1 = s.get(link)
        bs_content3 = bs(home_page1.content, "html.parser")
        courses.append(str(bs_content3.findAll("h1")[0]).split('-')[1].split('<')[0])
    
    courses1 = []
    count=0
    for i in courses:
        i = i+' '+"("+str(count)+")"
        courses1.append(i)
        count+=1
    print(courses1)
       
    
    user_given_course =     int(input("Enter the course number : "))            
       
    daterange = pd.date_range("2021-09-6", "2021-12-26")
    dates_list = [single_date.strftime("%Y %B %d") for single_date in daterange]
    selectio_dates_list=[]
    p=0
    q=6
    print(dates_list[p],'-',dates_list[q],"(1)")
    selectio_dates_list.append((dates_list[p],'-',dates_list[q]))
    count=2
    for i in range(len(dates_list)):
        try:
            p+=1
            q+=1
            p=p+6
            q=q+6
            print(dates_list[p],'-',dates_list[q]," ","("+str(count)+")")
            count+=1
            selectio_dates_list.append((dates_list[p],'-',dates_list[q]))
        except:
            pass
        
    user_given_session = input(" Enter the Section number : ")
    user_given_session = user_given_session.split()
    user_given_session = ["section-"+x for x in user_given_session]
    
    first_links=first_links[4:-1]
    final_links= []
    final_names= []
    print(' ')
    home_page1 = s.get(first_links[user_given_course])
    bs_content3 = bs(home_page1.content, "html.parser")
    
    for section in user_given_session:
        try:
            print("downloading ",section)
            for li in bs_content3.findAll("li",{"id":section}):
                for ui in li.findAll('a',{"class":"aalink"}):
                    # Extract file type
                    src = str(ui).split(' src')[1]
                    r1 =re.findall(r"=(.*)/>",src)[0]
                    if r1.split('/')[-1].split('-')[0] == 'pdf':
                        ext_name = '.pdf'
                    elif r1.split('/')[-1].split('-')[0] == 'powerpoint':
                        ext_name = '.pptx'
                    else:
                        ext_name = '.mp4'
                    
#                     print(ext_name)
                    
#                     final_links.append(ui['href'])
                    
                    for i in str(ui).split(">"):
                        try:
                            if i.split('<')[1] == 'span class="accesshide"':
                                final_names.append(i.split('<')[0].replace(" ","_")+ext_name)
                        except:
                            pass         
                  
                    
                    final_links.append(ui['href'])
        except:
            print("Unable to download ",section)
            pass
                      
 #-------------------------------------------------------------------------------------------------#       
    for index,link in enumerate(final_links):
        if link.split("/")[4] == 'lti':
            site = s.get(link)
            bs_content5 = bs(site.content, "html.parser")
            for k in bs_content5.findAll('div',{'class','container-fluid d-print-block'}):
                for l in k.findAll('div',{'class':'row pb-3 d-print-block'}):
                    for m in l.findAll('div',{'class':'col-12'}):
                        final = []
                        for i in str(m).split():
                            if i[:4]=='href':
                                final.append(i[6:-1])
                        lk = final[0]
        
                        final_links[index]=lk 
        
    
    for index,url in enumerate(final_links):
        if final_names[index][-3:]=='mp4':
            print(url,"only link as it is video")
            
            desktop = winshell.desktop()
            final_name = final_names[index][:-4]+".url"
            path = os.path.join(desktop, final_name)
            target = url
            shortcut = open(path, 'w')
            shortcut.write('[InternetShortcut]\n')
            shortcut.write('URL=%s' % target)
            shortcut.close()


        else:
            r = s.get(url, allow_redirects=True)
            print(url,final_names[index])
            filename = "C:\\Users\\91637\\Desktop\\downloaded moodle\\"+ final_names[index]
            open(filename , 'wb').write(r.content)
            
    print("xxxxxxxxxxxx")
    r = s.get('https://moodle.ubishops.ca/mod/lti/launch.php?id=83278')
    for response in r.history:
        print(response.url)
#             final_links[index] =convert_url(link)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
       

