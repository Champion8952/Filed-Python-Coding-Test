from flask import Flask, request, Response
from threading import Thread
from datetime import datetime
import time


APP = Flask(__name__)

class Payments:    
    ##Paymeny Gateway Declaration 
    PremiumPaymentGatewayThead = False
    ExpensivePaymentGatewayThread = False
    CheapPaymentGatewayThread = False
    
    def __init__(self):
        pass
    def CheapPaymentGateway(self, cardNo, amt):
        print("CheapPaymentGateway Called")
        ## Here We can call External Payment Service like Stripe, Razorpay, Paytm etc.
        time.sleep(5)
    def ExpensivePaymentGateway(self, cardNo, amt):
        print("ExpensivePaymentGateway Called")
        ## Here We can call External Payment Service like Stripe, Razorpay, Paytm etc.
        time.sleep(5)
    def PremiumPaymentGateway(self, cardNo, amt):
        print("PremiumPaymentGateway Called")
        ## Here We can call External Payment Service like Stripe, Razorpay, Paytm etc.
        time.sleep(5)

def sumDigits(digit):
    if digit < 10:
        return digit
    else:
        ## since the maximum single digit number could be 9 and the double will be 18 which sum is 9 
        ## and its maximum , that represents there is no need to multiple check it 
        sum = (digit % 10) + (digit // 10)
        return sum

def ValidateCreditCard(creditCard):
    ## To Validate Credit Card    
    if creditCard != None:
        creditCard = creditCard[::-1]
        creditCard = [int(x) for x in creditCard]
        doubledSecondDigitList = list()
        digits = list(enumerate(creditCard, start=1))
        
        for index, digit in digits:
            if index % 2 == 0:
                doubledSecondDigitList.append(digit * 2)
            else:
                doubledSecondDigitList.append(digit)

        doubledSecondDigitList = [sumDigits(x) for x in doubledSecondDigitList]
        sumDigit = sum(doubledSecondDigitList)
        if sumDigit % 10 == 0:
            return True
        else:
            return False
    else:
        return False

def ValidateExpirationCard(date):
    ## TO validate Expiration Card Date
    ## Not given in question to check for MM/YYYY format or DD/MM/YYYY

    if date!=None:
        date_format = "%d/%m/%Y"
        start = datetime.strptime(date, date_format)
        now = datetime.now()
        if start > now:
            return True
        else:
            return False
    else:
        return False

def ValidateAmount(amount):
    ## To validate amount 
    if amount!=None:
        if amount>=0:
            return True
        else:
            return False
    else:
        return False
       
def ValidateCardHolder(cardholder):
    if len(cardholder)>0:
        return True
    else:
        return False

## Route for Process Payment and POST API

@APP.route('/payments', methods=['POST'])
def ProcessPayment():
    # Fetching the values and validating them
    
    ## Credit Card Number is mentioned and it is mandatory
    CreditCardNum = request.form.get("CreditCardNumber",None)
    if ValidateCreditCard(CreditCardNum) == False:
        return Response("Invalid card number or card number not given",status=400)

    ## Card Holder Name Not in use but require to take the Name as Mandatory
    CardHolder = request.form.get("CardHolder",None)
    if ValidateCardHolder(CardHolder) == False:
        return Response("Name is Not Given",status=400)
    
    ## Expiry Date is mentioned and it is mandatory
    ExpirationDate = request.form.get("ExpirationDate",None)
    if ValidateExpirationCard(ExpirationDate) == False:
        return Response("Date is Invalid",status=400)
    
    ## Security Not in use optional
    SecurityCode =  request.form.get("SecurityCode",None)

    ## Amount is mentioned and it is mandatory
    amount = int(request.form.get("Amount",None))
    if ValidateAmount(amount) == False:
        return Response("Invalid Amount",status=400)

    ## To check for different payment gateway 
    if(amount <= 20):
        if(Payments.CheapPaymentGatewayThread==False):
            Payments.CheapPaymentGatewayThread = True
            Payments.CheapPaymentGateway(Payments,CreditCardNum, amount)
            Payments.CheapPaymentGatewayThread = False
            return Response("CheapPayment is Called",status=200)
        else:
            return Response("CheapPayment is in use please try after 5 seconds",status=500)
    elif(amount >= 21 and amount <= 500):
        if Payments.ExpensivePaymentGatewayThread==False:
            Payments.ExpensivePaymentGatewayThread = True
            Payments.ExpensivePaymentGateway(Payments, CreditCardNum, amount)
            Payments.ExpensivePaymentGatewayThread = False
            return Response("Expensive Payment is Called",status=200)
        elif Payments.CheapPaymentGatewayThread==False:
            Payments.CheapPaymentGatewayThread = True
            Payments.CheapPaymentGateway(Payments, CreditCardNum, amount)
            Payments.CheapPaymentGatewayThread = False
            return Response("Expensive Payment Gateway is in use so we are using Cheap Gateway",status=200)
        else:
            return Response("Expensive Gateway and Cheap gateway both are in use. Please try after sometime",status=500)
    else:
        if Payments.PremiumPaymentGatewayThead == False:
            Payments.PremiumPaymentGatewayThead = True
            Payments.PremiumPaymentGateway(Payments, CreditCardNum, amount)
            Payments.PremiumPaymentGatewayThead = False
            return Response("Premium payment is gateway called",status=200)
        else:
            for i in range(0,3):
                if Payments.ExpensivePaymentGatewayThread == False:
                    Payments.ExpensivePaymentGatewayThread = True
                    Payments.ExpensivePaymentGateway(Payments, CreditCardNum, amount)
                    Payments.ExpensivePaymentGatewayThread = False
                    return Response(f"Premium payment gateway is in use so Expensive called {i+1}-time",status=200)
                time.sleep(5)
            return Response("All gateways are busy",status=500)

if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=8000, debug=True)
