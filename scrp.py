import requests
from bs4 import BeautifulSoup
import smtplib


URL='https://store.steampowered.com/specials#tab=TopSellers'

header ={"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

page=requests.get(URL,headers=header)

soup= BeautifulSoup(page.content, 'html.parser')
all_details=[]
titles_topsellers = soup.find_all("div",{'id':'TopSellersRows'})
titles_newreleases= soup.find_all("div",{'id':'NewReleasesRows'})
titles_popular= soup.find_all("div",{'id':'ConcurrentUsersRows'})
def get_det(sp_obj):
    for title in sp_obj:
        titlename=title.find_all("div",{"class":"tab_item_name"})
        dsc=title.find_all("div",{"class":"discount_pct"})
        prc=title.find_all("div",{"class":"discount_final_price"})
        tit=title.find_all("div",{"class":"tab_item_top_tags"})
        org_prc=title.find_all("div",{"class":"discount_original_price"})
        game_link=title.find_all('a',href=True)
        
            
        
    for i in range(0,len(dsc)):
        tit_str=tit[i].get_text().split(',')
        temp=[titlename[i].get_text(),int(org_prc[i].get_text().replace('₹ ','').replace(',','')),int(dsc[i].get_text().replace('-','').replace('%','')),int(prc[i].get_text().replace('₹ ','').replace(',','')),tit_str]
        temp.append(game_link[i]['href'])
        all_details.append(temp)
        
get_det(titles_newreleases)
get_det(titles_topsellers)
get_det(titles_popular)
fin_det=[]
for det in all_details:
    if det[2]>=50 and det[3]<=400:
        fin_det.append(det)
        
fin_str=''
for i in fin_det:
    fin_str=fin_str+"\n\nName- "+i[0]+"\n"+"Original Price-Rs "+str(i[1])+"\t"+"Discounted Price-Rs "+str(i[3])+"\n"+"Discount Percentage-"+str(i[2])+"%"+"\n"
    genre=''
    for j in i[4]:
        genre=genre+j+","
        
    fin_str=fin_str+genre+"\nLink-"+i[5]
    

fin_str=fin_str.replace('®','')
    
    
def send_mail(fin_str):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('mukundacharya2020@gmail.com','cdxsfozsqkposogy')
    
    subject ="Todays list of Games On Sale!"
    
    body="The Games with more than 50% discount and less than Rs.400 are-"+"\n\n"+fin_str+"\n\n\nHappy Shopping!"
    
    
    msg= f"Subject: {subject}\n\n{body}"
    
    server.sendmail('mukundacharya2020@gmail.com','mukuacharya30@gmail.com',msg)
    print("Email has been sent!")
    server.quit()
    
    
    
send_mail(fin_str)
     
    
        

        
    
