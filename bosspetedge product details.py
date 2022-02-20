

import requests
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import smtplib
import re
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


# from email.MIMEMultipart import MIMEMultipart
# from email.MIMEText import MIMEText
# from email.MIMEBase import MIMEBase
from email import encoders
import os,sys
import mysql.connector
import time
l = []

def send_mail(s):
    mycursor = mydb.cursor()
    ############# fetch all the changes 
    mycursor.execute("select Product_Title,sku,product_price from bosspetedge_op where is_change=1")
    myresult = mycursor.fetchall()

    file_df = pd.DataFrame(l,columns=["newproduct"])
    file_df.to_excel("new_prod.xls",index=False)


    ############# creating file for email
    file_df = pd.DataFrame(myresult,columns=["Product_Title","sku","product_price"])

    file_df.to_excel("price_change.xls",index=False)         

    mycursor = mydb.cursor()
    ############# fetch all the changes 
    mycursor.execute("select Product_Title,sku,product_price from bosspetedge_op where discontinue=1")
    myresult = mycursor.fetchall()


    ############# creating file for email
    file_df = pd.DataFrame(myresult,columns=["Product_Title","sku","product_price"])

    file_df.to_excel("discontinue.xls",index=False)   

    mycursor = mydb.cursor()
    ############# fetch all the changes 
    mycursor.execute("select Product_Title,sku,category,sub_category,Product_link from bosspetedge_op where add_url=1")
    myresult = mycursor.fetchall()


    ############# creating file for email
    file_df = pd.DataFrame(myresult,columns=["Product_Title","sku","category","sub_category","url"])

    file_df.to_excel("bosspetedge_op.xls",index=False)


    fromaddr = "anandn@fcsus.com"
    # toaddr =  ["ajayb@fcsus.com","amitk@fcsus.com","talibd@fcsus.com"]
    toaddr =  "nishadaman4438@gmail.com"
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr

    msg['Subject'] = "Update in bosspetedge_op"
    
    body = s
    
    msg.attach(MIMEText(body, 'plain'))
    
    filename = "price_change.xls"
    attachment = open("price_change.xls", "rb")
    filename2 = "bosspetedge_op.xls"
    attachment2 = open("bosspetedge_op.xls", "rb")

    filename3 = "discontinue.xls"
    attachment3 = open("discontinue.xls", "rb")

    filename4 = "new_prod.xls"
    attachment4 = open("new_prod.xls", "rb")
    
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

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment3).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename3)
    msg.attach(part)

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment4).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename4)
    msg.attach(part)



    #server = smtplib.SMTP('smtp.gmail.com', 587)
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    #server.login(fromaddr, "fcsus@123")
    server.login(fromaddr, "Aman@123")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

try:    
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Anishad@123",
    database="abc"
    )
    mycursor = mydb.cursor()
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `bosspetedge_op` (
        `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `Product_Title` varchar(300) NOT NULL,
        `sku` varchar(200) NOT NULL ,
        `parent_sku` varchar(200) DEFAULT NULL,
        `primary_sku` varchar(200) DEFAULT NULL,
        `LMP_SKU` varchar(600) DEFAULT NULL,
        `UPC` varchar(15) DEFAULT NULL,
        `product_price` varchar(200) DEFAULT NULL ,
        `image1` varchar(500) DEFAULT NULL,
        `image2` varchar(500) DEFAULT NULL,
        `category` text,
        `sub_category` text,
        `Product_link` text,
        `add_url` text,
        `product_discription` text,
        `in_stock` int DEFAULT '0' ,
        `brand` varchar(50) NOT NULL,
        `long_discription` text,
        `sugg_price` int DEFAULT '0',
        `option_name` varchar(50),
        `notions_vnp` varchar(200) DEFAULT NULL,
        `previous_vnp` decimal(7,2) DEFAULT NULL,
        `vnp` decimal(7,2) DEFAULT NULL,
        `discontinue` varchar(200) DEFAULT '0',
        `is_change` varchar(200) DEFAULT '0'
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1""")
 


    # In[3]:



    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }


    # In[4]:


    mycursor.execute("select category,sub_category,url from bosspetedge_product_url  where processed=0 ")
    result = mycursor.fetchall()



    request_session = requests.session()

    resp = request_session.get("https://www.bosspetedge.com/")

    resp_soup = BeautifulSoup(resp.text,'lxml')

    form_key = resp_soup.find("input",{"name":"form_key"})["value"]

    loginlink = resp_soup.find("li",{"class":"authorization-link"}).find("a")["href"]

    data = {
    'form_key': form_key,
    'login[username]': 'dans@fcsus.com',
    'login[password]': '1Construction5#',
    'persistent_remember_me': 'on',
    'send': ''
    }

    response = request_session.post(loginlink, headers=headers, data=data)




    headers = {
        'authority': 'www.bosspetedge.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://www.bosspetedge.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.bosspetedge.com/za-smiling-toys',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }


    unicode = str

    def find_details(soup,pro,opt,opt1):
   
        Product_Title=''
        UPC=''
        brand=''
        suggested_price=''
        short_discription=''
        sku=''
        img=''
        price =''
        product_disc = ''
        in_stock = '0'
        suggested_price =''
        if soup.find("span",{"itemprop":"name"}):
            Product_Title = soup.find("span",{"itemprop":"name"}).text.replace("'","")
        if soup.find("td",{"data-th":"UPC"}):
            UPC = soup.find("td",{"data-th":"UPC"}).text

        if soup.find("td",{"data-th":"Brand"}):
            brand = soup.find("td",{"data-th":"Brand"}).text.replace("'","")


        if soup.find("span",{"class":"suggested-price"}):
            suggested_price = soup.find("span",{"class":"suggested-price"}).find_all("span")[-1].text.strip().replace("'","").replace("$","")


        if soup.find("p",{"class":"p1"}):
            short_discription = soup.find("p",{"class":"p1"}).text.replace("'","")

        if soup.find("div",{"itemprop":"description"}):
            short_discription = soup.find("div",{"itemprop":"description"}).text.replace("'","")

        if soup.find("div",{"itemprop":"sku"}):
            sku = soup.find("div",{"itemprop":"sku"}).text.replace("'","")

        if soup.find("meta",{"property":"og:image"}):
            img = soup.find("meta",{"property":"og:image"})["content"]

        if soup.find("span",{"data-price-type":"finalPrice"}):

            price = soup.find("span",{"data-price-type":"finalPrice"})["data-price-amount"]
            price=price.replace("$","")

        if soup.find("div",{"class":"product attribute description"}):
            product_disc = soup.find("div",{"class":"product attribute description"}).text.strip().replace("'","")

        # if soup.find("input",{"title":"Qty"}):
        #     in_stock =  soup.find("input",{"title":"Qty"})["value"]
        short_discription = unicode(short_discription).encode('ascii', 'ignore')
        short_discription=str(short_discription).replace(' "','').replace("'",'')

        product_disc = unicode(product_disc).encode('ascii', 'ignore')
        product_disc=str(product_disc).replace(' "','').replace("'",'')
        # print(product_disc)
        # sys.exit(0)
        if opt!=-1:
        #         for opt in range(len(soup.find_all("span",{"class":"description"}))):
            option_name = soup.find_all("span",{"class":"description"})[opt].text.replace("'","")
            option_sugg = soup.find_all("span",{"class":"suggested-retail"})[opt].text.replace("'","").replace("$","")
            option_sku =soup.find_all("input",{"class":"bulk-grid-input"})[opt1]["data-sku"].replace(" ","_")
        # option_price = soup.find_all("span",{"class":"price"})[opt]
            produt_id = soup.find_all("input",{"class":"bulk-grid-input"})[opt1]["data-product-id"]
            data = '{"productIds":['+produt_id+']}'
            response = request_session.post('https://www.bosspetedge.com/rest/V1/erp_list_price/', headers=headers, data=data)
            # option_price = json.loads(response.text)[0]["priceText"]
            # option_price=option_price.replace("$","")
            _option_price = json.loads(response.text)[0]["priceText"]
            if "Save" in _option_price:
                _pr=_option_price.split("|") 

                option_price= _pr[1]
            else:
                option_price= _option_price  

            stock = json.loads(response.text)[0]["text2"]
            if stock == "In Stock":
                in_stock = "1"
            else:
                in_stock = "0"#stock.strip().replace("'","")

            option_price=option_price.replace("$","")   
        # if not option_sugg.isnumeric():
            option_sugg='0' 
     
            l.append('BP01'+option_sku)
            sql = "insert into bosspetedge_op (Product_Title, sku , parent_sku ,  primary_sku,LMP_SKU , UPC ,notions_vnp, product_price,image1,category,sub_category,Product_link,add_url,product_discription ,in_stock ,brand,long_discription,sugg_price,option_name) value ('"+Product_Title+"', 'BP01"+option_sku+"' , 'BP01"+option_sku+"' ,  'BP01"+option_sku+"' , '"+sku+"' , '"+UPC+"' , '"+option_price+"' , '"+option_price+"','"+img+"','"+pro[0]+"','"+pro[1]+"','"+pro[2]+"',1,'"+short_discription+"' ,'"+in_stock+"','"+brand+"','"+product_disc+"','"+option_sugg+"','"+option_name+"')"
        #                 print(sql)
            mycursor.execute(sql)
            mydb.commit()
            
            
        else:
            #if not suggested_price.isnumeric():
    
            suggested_price='0'
            j = 'BP01'+sku.replace(" ","_")
            l.append(j)
            sql = "insert into bosspetedge_op (Product_Title, sku , parent_sku ,primary_sku,LMP_SKU   , UPC , product_price,image1,category,sub_category,Product_link,add_url,product_discription ,in_stock ,brand,long_discription,sugg_price,option_name) value ('"+Product_Title+"', 'BP01"+sku.replace(" ","_")+"' , 'BP01"+sku.replace(" ","_")+"' ,  'BP01"+sku.replace(" ","_")+"' , '"+sku+"' , '"+UPC+"' , '"+price+"','"+img+"','"+pro[0]+"','"+pro[1]+"','"+pro[2]+"',1,'"+short_discription+"' ,'"+in_stock+"','"+brand+"','"+product_disc+"','"+suggested_price+"','')"
        #                 print(sql)
            mycursor.execute(sql)
            mydb.commit()



    for pro in result:
    
        respo = request_session.get(pro[2],headers=headers)
        soup = BeautifulSoup(respo.text,"lxml")
        
        # print(soup)     
        # sys.exit()
        discoutinued = soup.find("h1").text
        if discoutinued == "WE'RE SORRY...":
            sql = "update bosspetedge_op set discontinue='1' where Product_link='"+pro[2]+"'"
            mycursor.execute(sql)
            mydb.commit()
        else:
            if soup.find_all("span",{"class":"description"}):
                # length=len(soup.find_all("span",{"class":"description"}))
                # print(length)
                # length1=len(soup.find_all("span",{"class":"description"})[2].parent.parent.find_all("input",{"class":"bulk-grid-input"}))
                # print(length1)
                # sys.exit('0')
                choice=0
                for opt in range(len(soup.find_all("span",{"class":"description"}))):
                
                    
                    for opt1 in range(len(soup.find_all("span",{"class":"description"})[opt].parent.parent.find_all("input",{"class":"bulk-grid-input"}))):
                     
                        option_name = soup.find_all("span",{"class":"description"})[opt].text.replace("'","")
                        option_sugg = soup.find_all("span",{"class":"suggested-retail"})[opt].text.replace("'","").replace("$","")
                        option_sku =soup.find_all("input",{"class":"bulk-grid-input"})[choice]["data-sku"]
                    # option_price = soup.find_all("span",{"class":"price"})[opt]
                        produt_id = soup.find_all("input",{"class":"bulk-grid-input"})[choice]["data-product-id"]
                        data = '{"productIds":['+produt_id+']}'
                        response = request_session.post('https://www.bosspetedge.com/rest/V1/erp_list_price/', headers=headers, data=data)
                        _option_price = json.loads(response.text)[0]["priceText"]
                        if "Save" in _option_price:
                            _pr=_option_price.split("|") 

                            option_price= _pr[1]
                        else:
                            option_price= _option_price  

                        if "|" in _option_price:
                            _pr=_option_price.split("|") 

                            pr= _pr[0].split('$')
                            option_price=pr[1]
                        else:
                            option_price= _option_price        
                        stock = json.loads(response.text)[0]["text2"]
                        if stock == "In Stock":
                            in_stock = "1"
                        else:
                            in_stock = "0"
                        
                        option_price=str(option_price).replace("$","").replace(" ","") 
                        # print(produt_id+ " "+option_price)

                        # sys.exit(0)
                        mycursor.execute("select product_price,in_stock from bosspetedge_op  where sku='BP01"+option_sku.replace(" ","_")+"'")
                        product_found = mycursor.fetchall()
                        if not product_found:
                            find_details(soup,pro,opt,choice)
                        if product_found:
                            if option_price != product_found[0][0]:

                                #if not option_sugg.isnumeric():
                                option_sugg='0'
                                sql = "update bosspetedge_op set previous_vnp=product_price , is_change=1,product_price='"+option_price+"',notions_vnp='"+option_price+"',option_name='"+str(option_name)+"',sugg_price='"+(option_sugg)+"' where sku='BP01"+option_sku.replace(" ","_")+"'"
                                mycursor.execute(sql)
                                mydb.commit()
                            if in_stock != product_found[0][1]:

                                sql = "update bosspetedge_op set in_stock='"+in_stock+"' where sku='BP01"+option_sku.replace(" ","_")+"'"
                                mycursor.execute(sql)
                                mydb.commit()
                        choice=choice+1        
                        
            else: 

                if soup.find("span",{"data-price-type":"finalPrice"}):
                    price = soup.find("span",{"data-price-type":"finalPrice"})["data-price-amount"]
                time.sleep(5)
                p_id=   soup.find("input",{"name":"product"})["value"]

                data = '{"productIds":['+p_id+']}'
                response = request_session.post('https://www.bosspetedge.com/rest/V1/erp_list_price/', headers=headers, data=data)
                option_price = json.loads(response.text)[0]["priceText"]
                option_price=str(option_price).replace("$","").replace(" ","") 
                stock = json.loads(response.text)[0]["text2"]
                if stock == "In Stock":
                    in_stock = "1"
                else:
                    in_stock = "0"
                

            
                if soup.find("div",{"itemprop":"sku"}):
                    sku = soup.find("div",{"itemprop":"sku"}).text.replace("'","").replace(" ","_")
                    p_id=   soup.find("input",{"name":"product"})["value"]

                    data = '{"productIds":['+p_id+']}'
                    response = request_session.post('https://www.bosspetedge.com/rest/V1/erp_list_price/', headers=headers, data=data)
                    _option_price = json.loads(response.text)[0]["priceText"]
                    if "Save" in _option_price:
                            _pr=_option_price.split("|") 

                            option_price= _pr[1]
                    else:
                        option_price= _option_price  

                    if "|" in _option_price:
                        _pr=_option_price.split("|") 

                        pr= _pr[0].split('$')
                        option_price=pr[1]
                    else:
                        option_price= _option_price  
                            

                    price=str(option_price).replace("$","").replace(" ","") 
                    
                    mycursor.execute("select product_price,in_stock from bosspetedge_op  where sku='BP01"+sku+"'")
                    product_found = mycursor.fetchall()
                    if not product_found:
                        find_details(soup,pro,opt=-1,opt1=-1)

                    if product_found:
                        if price != product_found[0][0]:

                            sql = "update bosspetedge_op set previous_vnp=product_price , is_change=1,product_price='"+price+"',notions_vnp='"+price+"' where sku='BP01"+sku+"'"
                            mycursor.execute(sql)
                            mydb.commit()
                        if in_stock != product_found[0][1]:
                            sql = "update bosspetedge_op set in_stock='"+str(in_stock)+"' where sku='BP01"+sku+"'"
                            mycursor.execute(sql)
                            mydb.commit()

        mycursor.execute("update bosspetedge_product_url  set processed=1 where url='"+pro[2]+"'")
        mydb.commit()
    s = "the boss_Op has succesfully run"
    send_mail(s)
except:
    s = "the boss_Op has unsuccesfully run"
    send_mail(s)



# sys.exit(0)



