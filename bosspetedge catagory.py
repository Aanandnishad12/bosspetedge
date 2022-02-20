
import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import smtplib


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from email.MIMEBase import MIMEBase
from email import encoders
import os
import mysql.connector





def anand():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anishad@123",
    database="mydatabase"
    )
    mycursor = mydb.cursor()
    mycursor.execute("""CREATE TABLE if not exists `bosspetedge_categories`(
        `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `category` varchar(250) NOT NULL,
        `sub_category` varchar(250) NOT NULL,
        `sub_sub_category` varchar(255) DEFAULT NULL,
        `url` text,
        `add_url` text,
        `processed` int(11) NOT NULL DEFAULT '0',
        `checked` int(11) NOT NULL DEFAULT '0'
    )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1""")
    mycursor.execute("ALTER TABLE andi.`bosspetedge_categories` CONVERT TO CHARACTER SET utf8")




    resp = requests.get("https://www.bosspetedge.com/see_all_categories/page/view")

    soup = BeautifulSoup(resp.text,'lxml')


    for h3 in range(len(soup.find_all("div",{"class":"category-listing-list-container"}))):
        category = soup.find_all("div",{"class":"category-listing-list-container"})[h3].find("h3").text
        for cate in range(len(soup.find_all("div",{"class":"category-listing-list-container"})[h3].find_all("a",{"class":"category-category-page-link"}))):
            product_url = soup.find_all("div",{"class":"category-listing-list-container"})[h3].find_all("a",{"class":"category-category-page-link"})[cate]["href"]
            sub_category = soup.find_all("div",{"class":"category-listing-list-container"})[h3].find_all("a",{"class":"category-category-page-link"})[cate].text.strip()
        
        
            mycursor.execute("select url from bosspetedge_categories where url='"+product_url+"'")
            url_found = mycursor.fetchall()
            if not url_found:
                print(url_found)
                # sql = "insert into bosspetedge_categories (category,sub_category,url,add_url,processed) value ('"+category+"','"+sub_category+"','"+str(product_url)+"','1','0')"
                # mycursor.execute(sql)
                # mydb.commit()
            if url_found:
                print(url_found)
                # mycursor.execute("update bosspetedge_categories set checked=1 where url='"+product_url+"'")
                # mydb.commit()




    resp = requests.get("https://www.bosspetedge.com/")

    soup = BeautifulSoup(resp.text,'lxml')



    for lv0 in range(len(soup.find_all("li",{"data-level":"level0"}))):
    #     print(lv0)
        category = soup.find_all("li",{"data-level":"level0"})[lv0].find("span").text
        # print(category)
        for lv1 in range(len(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"}))):
    #         print(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find("a",{"class":"header"}))
            level1 = soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find("a",{"class":"header"})
            if level1:            
    #             print(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find("span").text)
                sub_category = soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find("span").text
    #             print(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find("a",{"class":"header"})["href"])
            
            if len(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})) :
                for lv2 in range(len(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"}))):
        #             print(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2])
                    link = soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2]
                    if link:
        #                 print(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2].find("a",{"class":"category"}))
                        category_text = soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2].find("a",{"class":"category"})
                        text = soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2].find("a",{"class":"text"})
                        if category_text:
        #                     print(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2].find("a",{"class":"category"})["href"])
                            product_url = "https://www.bosspetedge.com"+soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2].find("a",{"class":"category"})["href"].replace("'","")
                            sub_sub_category = soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2].find("span").text.replace("'","")
        #                     print(soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2].find("span").text)
                        if text:
        #                     
                            product_url = "https://www.bosspetedge.com"+soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2].find("a",{"class":"text"})["href"].replace("'","")
                            sub_sub_category = soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find_all("li",{"data-level":"level2"})[lv2].find("span").text.replace("'","")
                    
                        mycursor.execute("select url from bosspetedge_categories where url='"+product_url+"'")
                        url_found = mycursor.fetchall()
                        if not url_found:

                            sql = "insert into bosspetedge_categories (category,sub_category,sub_sub_category,url,add_url,processed) value ('"+category+"','"+sub_category+"','"+sub_sub_category+"','"+str(product_url)+"','1','0')"
                            mycursor.execute(sql)
                            mydb.commit()
                        if url_found:
                            mycursor.execute("update bosspetedge_categories set checked=1 where url='"+product_url+"'")
                            mydb.commit()
            else:
                level1_category = soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find("a",{"class":"category"})
                if level1_category:
        #             print(len(level1_category))
                    sub_category =soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find("span").text.replace("'","")
                    product_url= "https://www.bosspetedge.com"+soup.find_all("li",{"data-level":"level0"})[lv0].find_all('li',{"data-level":"level1"})[lv1].find("a",{"class":"category"})["href"].replace("'","")

                    mycursor.execute("select url from bosspetedge_categories where url='"+product_url+"'")
                    url_found = mycursor.fetchall()
                    if not url_found:
                        sql = "insert into bosspetedge_categories (category,sub_category,url,add_url,processed) value ('"+category+"','"+sub_category+"','"+str(product_url)+"','1','0')"
            #             print(sql)
                        mycursor.execute(sql)
                        mydb.commit()
                    if url_found:
                        mycursor.execute("update bosspetedge_categories set checked=1 where url='"+product_url+"'")
                        mydb.commit()




    mycursor = mydb.cursor()
    ############# fetch all the changes 
    mycursor.execute("select category,sub_category,sub_sub_category,url from bosspetedge_categories where checked=0")
    myresult = mycursor.fetchall()
    ############# creating file for email
    file_df = pd.DataFrame(myresult,columns=["category","sub_category","sub_sub_category","url"])
    file_df.to_excel("category_removed.xls",index=False)



    mycursor = mydb.cursor()
    ############# fetch all the changes 
    mycursor.execute("select category,sub_category,sub_sub_category,url from bosspetedge_categories where add_url=1")
    myresult = mycursor.fetchall()
    ############# creating file for email
    file_df = pd.DataFrame(myresult,columns=["category","sub_category","sub_sub_category","url"])

    file_df.to_excel("category_added.xls",index=False)


# In[ ]:

def send_mail(s):
    fromaddr = "anandn@fcsus.com"
    # toaddr =  ["ajayb@fcsus.com","amitk@fcsus.com","talibd@fcsus.com"]
    toaddr =  "nishadaman4438@gmail.com"
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr

    msg['Subject'] = "bosspetedge categories"
    
    body = s
    
    msg.attach(MIMEText(body, 'plain'))
    
    filename = "category_removed.xls"
    attachment = open("category_removed.xls", "rb")

    filename2 = "category_added.xls"
    attachment2 = open("category_added.xls", "rb")

    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)



    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment2).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename2)
    msg.attach(part)



    #server = smtplib.SMTP('smtp.gmail.com', 587)
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    #server.login(fromaddr, "fcsus@123")
    server.login(fromaddr, "Aman@123")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
def main():
    try:
        anand()
        s = "bosspetedge_categories has run succesfully"
        send_mail(s)
        print(s)
    except:
        s = "bosspetedge_categories has run unsuccesfully"
        print(s)
if __name__ == "__main__":
    main()

