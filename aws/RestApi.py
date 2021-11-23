# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 12:07:15 2021

@author: AC
"""
import requests
  
# api-endpoint
URL = "https://exhtaawacg.execute-api.us-east-1.amazonaws.com/OCR/sqs"
  
# location given here
location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API
PARAMS = "00_00.jpg"
# PARAMS = {'address':location}
  
# sending get request and saving the response as response object
response = requests.post(url = URL, data  = PARAMS)
# extracting data in json format
data = response.json()
print(data)
