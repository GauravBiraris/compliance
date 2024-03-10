import streamlit as st  

       
### Global variables ###

pdf_files = {
   "Shop Act Registration": "Shop_Act.pdf",
   "GST Registration": "GST.pdf",
   "FSSAI License": "FSSAI.pdf",  
   "Legal Metrology": "Legal_Metrology.pdf",
   'EPF Employee Benefits': "EPF.pdf",
   "ISO 9001": "ISO_9001.pdf",
   'Maharshtra Shop Act Registration': "MHShop_act.pdf",
   'Maharshtra GST Registration': "GoM Gr.pdf",
   'Andhra Pradesh Shop Act Registration':'Andhra ShopAct.pdf',
   'State Shop Act Registration': "shop Act.pdf",
   'State GST Registration':'State GST Guidelines.pdf',
   'Legal Metrology certification for weights':'Legal M.pdf'
}
   
urls = {
   "Shop Act Registration": "https://example.com/shopact",
   "GST Registration": "https://www.gst.gov.in",
   'EPF Employee Benefits':'https://www.professionalutilities.com/epf-registration.php',
   'Legal Metrology certification for weights':'https://lm.doca.gov.in',
   "FSSAI License": "https://www.fssai.gov.in",
   "Legal Metrology": "https://legalmetrology.gov.in/",
   "EPF Registration":  "https://www.epfindia.gov.in/", 
   "ISO 9001": "https://iso.org/certification.html",
   'Maharshtra Shop Act Registration': "https://mahagov.gov.in",
   'Andhra Pradesh Shop Act Registration': 'https://www.indiacode.nic.in/bitstream/123456789/16396/1/act_no_20_of_1988.pdf',
   'Maharshtra GST Registration': "https://gst.gov.in",   
   'State GST Registration':"https://mahagst.gov.in/en/gst-act/240",
   'State Shop Act Registration':'https://mahakamgar.maharashtra.gov.in/lc-registration-of-shops-and-establishments.htm'
}

      
### Input widgets ###   

entity = st.selectbox("Business Entity", ["Sole Proprietor", "Partnership Firm", "LLP", "Private Limited Company"])

state = st.selectbox("State", ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya', 'Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal'])

sector = st.selectbox("Sector",["Transport", "Restaurant","Apparel","Grocery","Electronics","Agriculture", "Hardware"])

channel = st.radio("Channel",["Offline","Online","Offline + Online"])  

employees = st.slider("Number of Employees",0,100,10) 

revenue = st.slider("Annual Revenue (Lakh ₹)",1.0,200.0,5.0)

      
### Recommendation Logic ###

def get_mandatory(state,sector,entity,revenue):
   recs = ["GST Registration"]
    
   if state == "Assam":
      recs.append("Assam GST Registration")
   if state == "Maharashtra":
      recs.append("Maharshtra GST Registration")
      recs.append("Maharshtra Shop Act Registration")
   else:
      recs.append("State GST Registration")
      recs.append("State Shop Act Registration")

        
   if sector == "Restaurant": 
      recs.append("FSSAI License")
    
   if revenue >= 1.0:
      recs.append(f"{state} Shop Act Registration")
        
   return recs

def get_voluntary(entity, state, sector, employees, revenue):
   recs = []
    
   if employees >= 20 and sector != "Restaurant":
      recs.append("EPF Employee Benefits") 
    
   if revenue >= 10.0 and sector == "Grocery":
      recs.append("BIS Certification for better compliance")
      
   if sector == "Apparel" or 'Grocery':
      recs.append("Legal Metrology certification for weights")

   if state == "Maharashtra" and entity == "Partnership Firm":
      recs.append("Registration of partnership firms Registration")   

   return recs

      
### Display funtions ###

def show_recs(recs):
   for rec in recs:
      display_rec(rec)
    

def display_rec(rec):
   pdf = pdf_files[rec]
   url = urls[rec]  
    
   st.write("- " + rec)
   st.write(f"[Overview: {pdf}]")
   st.write(f"[Official website: {url}]")

      
### Main App Flow ###

if st.button("Get Recommendations"):
        
   mandatory = get_mandatory(state,sector,entity,revenue)  
   st.header("Mandatory Compliances")
   show_recs(mandatory)

   voluntary = get_voluntary(entity, state, sector, employees, revenue) 
   st.header("Voluntary Compliances")
   show_recs(voluntary)