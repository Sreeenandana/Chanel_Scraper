#importing required libraries
import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


#declaring global variables
data=[]
prize=[]
link=[]
size=[]
reference=[]
description=[]
title=[]
i=0
url="https://www.chanel.com/in/fragrance/bath-and-body/c/7x1x7x92/women/"
base_url='https://www.chanel.com'


#accessing the html content and parsing 
def scrape():
   global url
   response=requests.get(url)
   soup=BeautifulSoup(response.content,'lxml')
   product=soup.find_all('div', class_='txt-product')
   getLink(product)
   loadMore=soup.find('div', class_='container loadmore-container')
   temp_url=loadMore.find("a").attrs['href']
   if temp_url:
           url=base_url+temp_url
           scrape()


#extracting product links
def getLink(product):
   global i
   for p in product:
        product_url=base_url+p.find("a").attrs['href']
        link.append(product_url)
        response=requests.get(product_url)
        soup=BeautifulSoup(response.content,'lxml')
        getTitle(soup)
        getDescription(soup)
        getReference(soup)
        getPrize(soup)
        getSize(soup)
        i=i+1


#extracting product title
def getTitle(soup):
        title.append(soup.find('span', class_='heading product-details__title text-ltr-align').text.replace(" ","").replace("\n",""))

#extracting product description
def getDescription(soup): 
        description.append(soup.find('span', class_='product-details__description').text.replace(" ","").replace("\n",""))

#extracting product reference number
def getReference(soup):
        reference.append(soup.find('div', class_='product-details-block').text.replace(" ","").replace("\n",""))

#extracting product price
def getPrize(soup):
        prize.append(soup.find('p', class_='product-details__price').text.replace(" ","").replace("\n",""))

#extracting product size
def getSize(soup):
        size.append(soup.find('div', class_='product-details__option').text.replace(" ","").replace("\n",""))


#saving the output
def save_output():
   df = pd.DataFrame(list(zip(link,title,description,reference,prize,size)),
               columns =['LINK','TITLE','DESCRIPTION','REFERENCE','PRICE','SIZE'])
   df
   df.to_csv("chanel_output.csv")


#main function
def main():
   scrape()
   save_output()


if __name__ == "__main__":
    main()
