# FiledPythonCodingTest

# Running this code instruction
1. Python processpayment_api.py (This is the main API)

2. Python sample_test.py (This is a Simple Test python file)
   
   OR
   
   For Calling this processpayment_api.py , we can check using Postman also.
	First , Run the processpayment_api.py in background on local server
	Second , On Postman, It will be a POST request and URL will be localhost:8000/payments
   
   A Postman screenshot is attached in the folder , as Test_Postman.png

For Payment gateways I have created functions but not used any external payment gateway , but the gateways such as (Razorpay, Paytm, Stripe ,Instamojo etc) can be included as a test account using with Public and Publishable Key . Each payment gateway will run for 5 seconds .

If any query , do contact me .