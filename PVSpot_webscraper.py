"""
Accesses the SolarGIS website to download PVSpot data for various sites

@author: TeaganO
"""
#----------------------------------- imports ----------------------------------

#for interacting with Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *

#for pausing at times
from time import sleep

#to create folder to drop downloads
import os


#------------------------------definitions------------------------------
  
#monthly downloader
def access_website_monthly(sites_to_query,first_month,last_month,save_folder):

    #if save_folder doesn't exist, create it    
    try:
        os.mkdir(save_folder)
    except FileExistsError:
        pass

    #set up chrome options to use the specified folder for downloads
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : save_folder}
    chrome_options.add_experimental_option('prefs', prefs)
    #open driver instance with custom option
    driver = webdriver.Chrome(chrome_options=chrome_options)
   
    try:
      	 #load the website
        driver.get('https://solargis.info/pvspot/system-24/month.htm')
        driver.display=True
        sleep(2)

        #find login button        	        
        search_field = driver.find_element_by_id("loginLink").click()
        
        #log in
        search_field = driver.find_element_by_name("j_username")
        search_field.send_keys("hjalmar.russouw@energypartners.co.za")
        search_field = driver.find_element_by_name("j_password")
        search_field.send_keys("EPSolar8908%")
        
        #click sign in 
        search_field = driver.find_element_by_xpath('//button[text()="Sign in"]')
        search_field.send_keys(Keys.ENTER)
        
        #loop through the chosen sites from the gui 
        for site in sites_to_query:
            
            try:
                #choose the current site
                search_field = driver.find_element_by_partial_link_text(site).click() #click on site
                   
                #loop through the months chosen
                for mnth in range(first_month,last_month+1):
 
                    #set up month number to be used to find the right month on the website dropdown
                    month_number = "option[" + str(mnth) + "]"
                    
                    #select month number
                    #clear the search_field, try to find it, and try again if it fails
                    search_field=None
                    while search_field is None:
                        try:
                            search_field = driver.find_element_by_xpath('//*[@id="content"]/table/tbody/tr[1]/td[3]/select[2]/'+ month_number)
                        except NoSuchElementException as e:
                            pass
                    search_field.click()
                    
                    #click download button
                    #clear the search_field, try to find it, and try again if it fails
                    search_field=None
                    while search_field is None:
                        try:                    
                            search_field = driver.find_element_by_partial_link_text("Data in XLS format")
                        except NoSuchElementException as e:
                           # print(e.__class__.__name__)
                            pass
                    search_field.click()
            					
            #for sites that are greyed out - ignore them and move to the next one
            except ElementNotVisibleException as e:
                continue

    except Exception as e:
        print(e)
    
    finally:   
        sleep(3)
        driver.close()
        print('\nFinished.')
        
        
        
        
        
#------------------------------- yearly scraper -------------------------------
        
def access_website_yearly(sites_to_query,first_year,last_year,save_folder):
    

    #set folder path for downloads to be saved in
 #   new_folder="I:\A SOLAR PV\Commercial PV\PLANT MONITORING\Archive\Data\Yearly data"   

    #if folder doesn't exist, create it    
    try:
        os.mkdir(save_folder)
    except FileExistsError:
        pass

    #set up chrome options to use the specified folder for downloads
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : save_folder}
    chrome_options.add_experimental_option('prefs', prefs)
    #open driver instance with custom option
    driver = webdriver.Chrome(chrome_options=chrome_options)
   
    try:
      	#load the website
        driver.get('https://solargis.info/pvspot/system-24/month.htm')
        driver.display=True
        sleep(2)

        #find login button        	        
        search_field = driver.find_element_by_id("loginLink").click()
        
        #log in
        search_field = driver.find_element_by_name("j_username")
        search_field.send_keys("hjalmar.russouw@energypartners.co.za")
        search_field = driver.find_element_by_name("j_password")
        search_field.send_keys("EPSolar8908%")
        
        #click sign in 
        search_field = driver.find_element_by_xpath('//button[text()="Sign in"]')
        search_field.send_keys(Keys.ENTER)
        
        #click on first site just to ensure that the yearly view button is visible        
        search_field = driver.find_element_by_partial_link_text(sites_to_query[0]).click()
        
        #choose yearly view
        search_field=driver.find_element_by_partial_link_text("Yearly view").click()
        
    
        #loop through the chosen sites from the gui 
        for site in sites_to_query:
        
            try:
                #choose the current site
                search_field = driver.find_element_by_partial_link_text(site).click()  #click on site
        
                #select the drop down year menu
                year_dropdown = Select(driver.find_element_by_id('years'))
        
                for year in range(first_year,last_year+1):
                    
                    #to choose the year - will try all the years in the chosen range but will skip those that don't work
                    try:                    
                        year_dropdown.select_by_value(str(year)) #select year by value
                        
                        #click the download xls file
                        #clear the search_field, try to find it, and try again if it fails
                        search_field=None
                        while search_field is None:
                            try:                    
                                search_field = driver.find_element_by_partial_link_text("Data in XLS format")
                            except NoSuchElementException as e:
                                pass
                            
                        search_field.click()
                        
                    #for skipping year choices that don't work                
                    except NoSuchElementException as e:
                        continue
                    					
            #for sites that are greyed out - ignore them and move to the next one
            except ElementNotVisibleException as e:
                continue

    except Exception as e:
        print(e)
    
    finally:   
        sleep(3)
        driver.close()        
        print('\nFinished.')

        
        

        