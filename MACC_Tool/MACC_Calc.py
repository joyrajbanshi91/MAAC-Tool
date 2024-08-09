# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 20:33:52 2023

@author: Joy
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename


def btn_clicked():

    label.config(text="Please Select the input file")    
    
    Openfile=askopenfilename(filetypes=[("csv file","*.csv")],defaultextension=".csv")
    df = pd.read_csv(Openfile)
    
    df['Net_Cash_Flow']=df['Annual_Saving']-df['Annual_OpEx']
    
    NPV=[]
    Tot_Abatement=[]
    
    for i in df.index:
        factor=(df['Interest_Rate'][i])/100
        year=df['Project_Duration'][i]
        Discount_Cashflow=[]
        Discount_Emission=[]
        old_factor=1
        Initial_cashflow=df['Initial_Capital'][i]
        Initial_Disc_Emissions=df['Annual_Emission_Reduction'][i]
        Annual_Pay=df['Annual_Pay'][i]
        Finance_Period=df['Annual_Finance_Period'][i]
        c=0    
        for j in range (0,year,1):
            new_discount=old_factor*(1+factor)
            if c<Finance_Period:
                cashflow=(((df['Net_Cash_Flow'][i])-Annual_Pay)/new_discount)-Initial_cashflow
                F_Discount_Emissions=Initial_Disc_Emissions/new_discount
                Initial_cashflow=0
                old_factor=new_discount
                Discount_Cashflow.append(cashflow)
                Discount_Emission.append(F_Discount_Emissions)
            else:
                cashflow=(((df['Net_Cash_Flow'][i]))/new_discount)-Initial_cashflow
                F_Discount_Emissions=Initial_Disc_Emissions/new_discount
                Initial_cashflow=0
                old_factor=new_discount
                Discount_Cashflow.append(cashflow)
                Discount_Emission.append(F_Discount_Emissions)
            c+=1
    
            
        Tot_cashflow=np.sum(np.array(Discount_Cashflow))
        Tot_Disc_Emission=np.sum(np.array(Discount_Emission))
        NPV.append(Tot_cashflow)
        Tot_Abatement.append(Tot_Disc_Emission)
    
    df["NPV"]=np.array(NPV)
    df["Total_Abatement"]=np.array(Tot_Abatement)
    
    df["MAC"]=(df["NPV"]/df["Total_Abatement"])*(-1)
      

    ###################  For Plotting  ######
    label.config(text="Here is the MAAC Figure")
    
    df1=pd.DataFrame(df)
    df1.sort_values('MAC',inplace=True)
    
    w=df1['Total_Abatement'].to_list()
    
    xticks=[]
    for n, c in enumerate(w):
        xticks.append(sum(w[:n]) + w[n]/2)
        
    
    plt.figure(figsize = (10, 6))
    plt.rcParams["font.size"] = 12
    
    a = plt.bar(xticks, height = df1['MAC'], width = w, color=df1['Colour'], alpha = 0.8)
    plt.legend(a.patches, df1['Interventions'],fontsize=10)
    plt.xlabel("GHG emissions abatement (MtCO$_2e$)")
    plt.ylabel("Costs per GHG emissions reduction (INR/MtCO$_2e$)")
    plt.ticklabel_format(useOffset=False, style='plain')
    plt.tight_layout()
    plt.show()

################ Saving the output file #################

    label.config(text="Please save the output file")  
    file=asksaveasfilename(filetypes=[("csv file","*.csv")],defaultextension=".csv")
    df.to_csv(file, index=False)
    label.config(text="Processing over! The output file has been saved into the user-defined directory. Thanks!")

########### Tk Inter Gui starts from Here.. ###############

window = Tk()
window.title("Marginal Abatement Cost Curve Calculator")
window.geometry("1093x648")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 648,
    width = 1093,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 630, y = 350,
    width = 220,
    height = 72)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    550, 350,
    image=background_img)

label=Label(text="", font=('Calibri 15'))
label.place(
    x= 200 , y = 550,
    width = 600,
    height = 30
)
label.pack()

window.resizable(False, False)
window.mainloop()




