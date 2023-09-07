#importing required libraries
import requests
import csv
from bs4 import BeautifulSoup


#declaring global variables
data=[]
pr=[]
li=[]
si=[]
re=[]
de=[]
ti=[]
i=0
url="https://www.chanel.com/in/fragrance/bath-and-body/c/7x1x7x92/women/"
base_url='https://www.chanel.com'

#accessing the html content and parsing 
def scrap():
   global url
   res1=requests.get(url)
   soup1=BeautifulSoup(res1.content,'lxml')
   con=soup1.find_all('div', class_='txt-product')
   links(con)
   co=soup1.find('div', class_='container loadmore-container')
   temp_url=co.find("a").attrs['href']
   if temp_url:
           url=base_url+temp_url
           scrap()
   
#To extract links
def links(con):
   global i
   for c in con:
        lin=c.find("a").attrs['href']
        lin=base_url+lin
        li.append(lin)
        res2=requests.get(lin)
        soup=BeautifulSoup(res2.content,'lxml')
        title(soup)
        description(soup)
        reference(soup)
        prize(soup)
        size(soup)
        i=i+1

#To extract titles
def title(soup):
        ti.append(soup.find('span', class_='heading product-details__title text-ltr-align').text.replace(" ","").replace("\n",""))

#To extract description
def description(soup): 
        de.append(soup.find('span', class_='product-details__description').text.replace(" ","").replace("\n",""))

#To extract reference number
def reference(soup):
        re.append(soup.find('div', class_='product-details-block').text.replace(" ","").replace("\n",""))

#To extract price
def prize(soup):
        pr.append(soup.find('p', class_='product-details__price').text.replace(" ","").replace("\n",""))

#To extract size
def size(soup):
        si.append(soup.find('div', class_='product-details__option').text.replace(" ","").replace("\n",""))

#To save outut in a csv file
def save_out():
    row_head=['LINK','TITLE','DESCRIPTION','REFERENCE','PRICE','SIZE']
    for l,t,d,r,p,s in zip(li,ti,de,re,pr,si):
        data.append(l)
        data.append(t)
        data.append(d)
        data.append(r)
        data.append(p)
        data.append(s)
    rows = [data[i:i+6] for i in range (0, len(data),6)]
    with open('chanel.csv','a+', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(row_head)
        csvwriter.writerows(rows)

#main function
def main():
   scrap()
   save_out()

if __name__ == "__main__":
    main()
