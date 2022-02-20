

import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import smtplib
import re

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
    passwd="Anishad@123",
    database="abc"
    )
    mycursor = mydb.cursor()
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `bosspetedge_product_url` (
    `id` int NOT NULL AUTO_INCREMENT,
    `product_id` varchar(255) DEFAULT NULL,
    `category` varchar(250) NOT NULL,
    `sub_category`  varchar(250) NOT NULL,
    `product_name` varchar(250) NOT NULL,
    `url` text,
    `processed` int(11) NOT NULL DEFAULT '0',
    `add_url` text,
    KEY `id` (`id`)
    )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1""")





    mycursor.execute("select category,sub_category,url from bosspetedge_categories  where processed=0")
    result = mycursor.fetchall()




    for ul in result:
       
        response = requests.get(ul[2])
        soup = BeautifulSoup(response.text,'lxml')
        for prod in range(len(soup.find_all("li",{"class":"item product product-item"}))):
            
    #         print(soup.find_all("li",{"class":"item product product-item"})[prod].find("a")["href"])
    #         print(soup.find_all("li",{"class":"item product product-item"})[prod].find("p",{"class":"product sku product-item-sku"}).text.strip())
            product_url = soup.find_all("li",{"class":"item product product-item"})[prod].find("a")["href"].replace("'","")
            product_id = soup.find_all("li",{"class":"item product product-item"})[prod].find("p",{"class":"product sku product-item-sku"}).text.strip().replace("'","")

            product_name = soup.find_all("li",{"class":"item product product-item"})[prod].find("strong").text.strip().replace("'","")
            mycursor.execute("select product_id from bosspetedge_product_url  where product_id='"+product_id+"'")
            product_found = mycursor.fetchall()
            if not product_found:
             
                sql = "insert into bosspetedge_product_url (product_id,category,sub_category,product_name,url,processed,add_url) VALUES('"+product_id+"','"+ul[0]+"','"+ul[1]+"','"+product_name+"','"+product_url+"','0','1') "
                mycursor.execute(sql)
                mydb.commit()

            
            
        next_page =True
        npage = soup.find("li",{"class":"item pages-item-next"})
        if not npage:
            next_page =False

        while next_page:
            next_link = soup.find("li",{"class":"item pages-item-next"}).find("a")["href"]
    #         print(next_link)
            response = requests.get(next_link)
            soup = BeautifulSoup(response.text,'lxml')
            npage = soup.find("li",{"class":"item pages-item-next"})
            for prod in range(len(soup.find_all("li",{"class":"item product product-item"}))):
                product_url = soup.find_all("li",{"class":"item product product-item"})[prod].find("a")["href"].replace("'","")
                product_id = soup.find_all("li",{"class":"item product product-item"})[prod].find("p",{"class":"product sku product-item-sku"}).text.strip().replace("'","")
                product_name = soup.find_all("li",{"class":"item product product-item"})[prod].find("strong").text.strip().replace("'","")
                
                
                mycursor.execute("select product_id from bosspetedge_product_url  where product_id='"+product_id+"'")
                product_found = mycursor.fetchall()
                if not product_found:
                   
                    sql = "insert into bosspetedge_product_url (product_id,category,sub_category,product_name,url,processed,add_url) VALUES('"+product_id+"','"+ul[0]+"','"+ul[1]+"','"+product_name+"','"+product_url+"','0','1') "
                    mycursor.execute(sql)
                    mydb.commit()
            if not npage:
                next_page =False
        
        
        mycursor.execute("update bosspetedge_categories set processed=1 where url='"+ul[2]+"'")
        mydb.commit()




    mycursor = mydb.cursor()
    ############# fetch all the changes 
    mycursor.execute("select product_id,category,sub_category,product_name,url from bosspetedge_product_url where add_url=1")
    myresult = mycursor.fetchall()


    ############# creating file for email
    file_df = pd.DataFrame(myresult,columns=["product_id","category","sub_category","product_name","url"])

    file_df.to_excel("bosspetedge_product_added.xls",index=False)


def send_mail(s):

    fromaddr = "anandn@fcsus.com"
    # toaddr =  ["ajayb@fcsus.com","amitk@fcsus.com","talibd@fcsus.com"]
    toaddr =  "nishadaman4438@gmail.com"
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr

    msg['Subject'] = "bosspetedge product added"
    
    body = "bosspetedge product added "
    
    msg.attach(MIMEText(body, 'plain'))
    
    filename = "bosspetedge_product_added.xls"
    attachment = open("bosspetedge_product_added.xls", "rb")


    
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
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
        s = "bosspetedge_product url has run succesfully"
        send_mail(s)
    except:
        s = "bosspetedge_product url has run unsuccesfully"
        print
if __name__ == "__main__":
    main()

