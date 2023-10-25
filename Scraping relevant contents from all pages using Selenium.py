#!/usr/bin/env python
# coding: utf-8

# In[21]:


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


# In[22]:


options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")    #prevents sandbox issues
# options.add_argument("--headless")    #run chrome in headless (non-GUI) mode
# options.add_argument("--disable-gpu") #useful in headless mode to avoid GPU-related issues
#options.add_argument("--disable-dve-shm-usage")


# In[23]:


driver = webdriver.Chrome(options = options)
web = 'https://www.audible.com/adblbestsellers?ref_pageloadid=CI03XYkeT5d40w8B&ref=a_adblbests_t1_navTop_pl0cg1c0r0&pf_rd_p=6fb0ac98-e9fb-4acd-8278-aa237978ed3e&pf_rd_r=Z1QJCFJ38ZJPG3059S3D&pageLoadId=aIV9gmRDCSrzAYTB&ref_plink=not_applicable&creativeId=1642b4d1-12f3-4375-98fa-4938afc1cedc'
driver.get(web)
driver.maximize_window()  #for displaying the window all over the screen


# In[24]:


pagination = driver.find_element(By.XPATH,"//ul[contains(@class,'pagingElements')]")    #here we find the whole block representing pagination
pages = pagination.find_elements(By.TAG_NAME,'li')                                  #by this we point out the individual points in the pagination option
last_page_text = pages[-2].text
last_page = int(last_page_text)

current_page = 1

book_title = []
book_author = []
book_length = []

while current_page <= last_page:
  time.sleep(2)
  container = driver.find_element(By.CLASS_NAME,'adbl-impression-container') #we find the container that contains all the audio books in that page
  products = container.find_elements(By.XPATH,'.//li[contains(@class,"productListItem")]')   #here the . denotes the current context & the / denotes the immediate li tag



  for product in products:
    book_title.append(product.find_element(By.XPATH,".//h3[contains(@class,'bc-heading')]").text)
    book_author.append(product.find_element(By.XPATH,".//li[contains(@class,'authorLabel')]").text)
    book_length.append(product.find_element(By.XPATH,".//li[contains(@class,'runtimeLabel')]").text)

  try:
    current_page = current_page + 1  
    next_page = driver.find_element(By.XPATH,"//span[contains(@class,'nextButton')]")
    next_page.click()
  except:
    pass

driver.quit()


# In[25]:


df_books = pd.DataFrame({'Title': book_title,'Author': book_author,'Length': book_length})
df_books.to_csv('books.csv', index = False)

