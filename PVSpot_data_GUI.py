"""
Prompts user to choose sites and months to download PVSpot data for.
Then calls webscraper to run downloads.

@author: TeaganO
"""
#----------------------------------- imports ----------------------------------
#webscraper
import PVSpot_webscraper

#for GUI
from tkinter import *

#for checking chosen time exsits
import datetime
import dateutil.relativedelta

#for arranging objects on GUI correctly
import math

#------------------------------definitions------------------------------
'''check button class for sites'''
#to create and configure a check button for each available site
class site_checkbox:
    
    def __init__ (self,name):
        self.var=IntVar()   #set site's variable to an int type var
        self.name=name      #set site's name to the name provided when initialisied
        
    #make a checkbox on the gui corresponding to the site    
    #set its commmand to the add_delete_item method
    def make_checkbox(self,master,r,c):
        chkbut=Checkbutton(master, text=str(self.name),variable=self.var,command=self.add_delete_item).grid(row=r,column=c,sticky=W)
        
    #method to add or remove a site name from the sites_to_query list according to its checkbox state
    def add_delete_item(self):
        status=self.var.get()   #get the current state of the checkbutton
        if status == 1:         #if the checkbutton is checked, add the site name to the sites_to_query list
            sites_to_query.append(self.name)            
        elif status==0:         #if the checkbutton is unchecked, remove the site name from the sites_to_query list
            sites_to_query.remove(self.name)            


#function that is called when the OK button is pressed - closes the gui and allows for the programme to continue
def close_continue():
    form.destroy

#------------------------------------------------------------------------

'''set up site and month options'''

#dictionary of month names and their corresponding numbers
month_numbers={"January":1, "February":2,"March":3,"April":4,"May":5, "June":6,"July":7,"August":8,"September":9,"October":10,"November":11,"December":12}

#sites available on the website - will need editing when the site changes
site_options=["1. Lephalale Mall","2. Lephalale Mall","3. Lephalale Mall","Attacq LWB 1","Attacq LWB 2","Attacq LWB 3","Attacq LWB 4","Attacq LWB 5","Mpact Wadeville - 1","Mpact Wadeville - 2","Mpact Wadeville - 3","Mpact Wadeville - 4","Netcare - Akasia 2","Netcare - Akasia 3","Netcare - Akasia 4","Netcare - Akasia 5","Netcare - Akasia South","Netcare - Clinton 1","Netcare - Clinton 2","Netcare - Clinton 3","Netcare - Clinton 4","Netcare - LM 1","Netcare - LM 2","Netcare - Mulbarton 1","Netcare - Mulbarton 2","Netcare - Mulbarton 3","Netcare - Mulbarton 4","Netcare - N17 1","Netcare - N17 2","Netcare - SWP1","Netcare - SWP2","Netcare - SWP3","Netcare - SWP4","PCM - Tshikondeni","PNP Longmeadow - 1",
              "PNP Longmeadow - 2","PNP Longmeadow - 3","PNP Longmeadow - 4","PNP Longmeadow - 5","SAFT KG","SAFT Paarl - 1","SAFT Paarl - 2","SAFT Paarl - 3","SAFT Paarl - 4","Stellenpak 1","Stellenpak 2","Attacq GF 6","PNPC - Hurlingham","PNPC - Longmeadow DC OLD","PNPC - Philippi DC","PNR Aeroton 1","PNR Aeroton 2","PNR Bloem Bakery 1","PNR Bloem Bakery 2","PNR Bloem Bakery 3","PNR Bloem Bakery 4","PNR Bloem Bakery 5","PNR CFJ 1","PNR CFJ 2","PNR Pronutro 1","PNR Pronutro 2","PNR Clayville 1","PNR Clayville 2","PNR Clayville 3","PNR Clayville 4","PNR Clayville 5","PNR Clayville 6","Attacq - MRM 1","Attacq - MRM 2","Attacq - MRM 3","Fruit & Veg JHB",
              "PNR Klerksdorp Mill 1","PNR Klerksdorp Mill 2","PNR Klerksdorp Mill 3","PNR Klerksdorp Mill 4","PNR Klerksdorp Mill 5","PNR Klerksdorp Mill 6","PNR Klerksdorp Mill 7","PNR SAD Treefruit","Quantum Sova PS","Van Loveren"]

#list of sites chosen from the gui
sites_to_query=[]


'''set up GUI'''
#create tkinter gui window
form = Tk() 
form.title("PVSpot automated download")
form.geometry("650x640")    #wxh

#create frames on the form
top_frame=Frame(form)
top_frame.pack(side=TOP)

left_frame=Frame(form)     #creates frame (left_frame) on the window (form) and allows us to hold other widgets
left_frame.pack(side=LEFT)         #place into form window

bottom_frame=Frame(form)
bottom_frame.pack(side=BOTTOM)


#create month to and from dropdowns
selected_month_to=StringVar()
selected_month_from=StringVar()

previous_month=(datetime.datetime.now()+ dateutil.relativedelta.relativedelta(months=-1)).strftime("%B")
selected_month_to.set(previous_month)    #set default to current month
selected_month_from.set(previous_month)    #set default to current month

month_from=OptionMenu(top_frame,selected_month_from,*month_numbers).grid(row=1,column=1,sticky=W)
month_to=OptionMenu(top_frame,selected_month_to,*month_numbers).grid(row=1,column=3,sticky=W)


#create labels for month selection
label0 = Label(top_frame,text="Choose the months to download:").grid(row=0,column=0,columnspan=3,sticky=W) 
label1 = Label(top_frame,text="Month from:").grid(row=1,column=0,sticky=W) 
label2 = Label(top_frame,text="Month to:").grid(row=1,column=2,sticky=W) 



#-------------------------- year inputs ---------------------------------------
#
#label3=Label(top_frame,text="Year from:").grid(row=0,column=4,padx=10,sticky=W)
#label3=Label(top_frame,text="Year to:").grid(row=1,column=4,padx=10,sticky=W)
#first_year=Entry(top_frame).grid(row=0,column=5,sticky=E)
#last_year=Entry(top_frame).grid(row=1,column=5,sticky=E)


#label for sites
label3 = Label(top_frame,text="Choose which sites you'd like to download data for:")
label3.grid(row=2,column=0,columnspan=3,sticky=W)   

#counter for positioning site names
i=0

#site check boxes - loop through and place on GUI, shifting to the next column when the current column fills up
for name in site_options:
    current_site=site_checkbox(name)
    if i<math.floor(len(site_options)/4):
        current_site.make_checkbox(left_frame,i,0)
    elif i>=math.floor(len(site_options)/4) and i< math.floor(2*len(site_options)/4):
        current_site.make_checkbox(left_frame,(i-math.floor(len(site_options)/4)),1) 
    elif i>=math.floor(2*len(site_options)/4) and i< math.floor(3*len(site_options)/4):
        current_site.make_checkbox(left_frame,(i-math.floor(2*len(site_options)/4)),2) 
    elif i>=math.floor(3*len(site_options)/4):
        current_site.make_checkbox(left_frame,(i-math.floor(3*len(site_options)/4)),3) 
    i+=1


#create quite button
quit_button=Button(left_frame, text="OK", command=form.destroy).grid(row=math.ceil(len(site_options)/4),column=2)

#-------------------------------- end of creating GUI -------------------------

'''open up GUI'''
form.mainloop() #display on screen continuously

#------------------- now for actually downloading data ------------------------
'''download raw data'''

if len(sites_to_query)==0:
    #alert user no sites were selected
    print("No sites selected, start again.")
else:
    #determine what month we are currently in
    current_month=int(datetime.datetime.now().strftime("%m"))

    #retrieve the requested months from the GUI
    first_month=month_numbers[selected_month_from.get()]
    last_month=month_numbers[selected_month_to.get()]

    #if either of the selected months is beyond the current month, reset it to the current month
    if first_month > current_month:
        first_month=current_month
    
    if last_month > current_month:
        last_month=current_month
       
    #call the webscraper to do the downloads 
    PVSpot_webscraper.access_website_monthly(sites_to_query,first_month,last_month,"I:\A SOLAR PV\Commercial PV\PLANT MONITORING\Archive\Data") 
    #end of downloading raw data
 
    
print("Closed")



