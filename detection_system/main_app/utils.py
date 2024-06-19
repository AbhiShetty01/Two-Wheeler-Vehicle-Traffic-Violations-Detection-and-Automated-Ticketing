from twilio.rest import Client
import yagmail

def send_challan(data):
    try:
        yag = yagmail.SMTP("autoemailsender2@gmail.com", "tczewxnxfrpviped")

        account_sid = "AC83b73636695eb2dfd406d70f4a589402"
        auth_token = "3c57d9f6dca93faedf5a60aca62521d4"
        client = Client(account_sid, auth_token)
        helmet = data["helmet_status"]
        plateNumber = data["plate_number"]
        noOfPassengers = data["no_of_passengers"]

        amount = 0
        challanBreaked = ''
        if helmet=="Not Wearing":
            amount = amount + 500
            challanBreaked = challanBreaked + '<br><br><b>Not Wearing Helmet (500 Rs)</b>'

        if noOfPassengers!='':
            if int(noOfPassengers)>=3:
                amount = amount + 1000
                challanBreaked = challanBreaked + '<br><br><b>There were 3 Passengers in your vehicle (1000 Rs)</b>'
        

        message = "Hi, User<br><br>You have break the following traffic rules "+challanBreaked+"<br><br>Now you have to pay <b>"+str(amount)+"Rs.</b> as Challan."
        #data = open(f"./main_app/static/{data['img']}").read().split('\n')
        yag.send(to='vishwanathn886@gmail.com', subject="Traffic Rule Challan", contents=message)
        yag.close()
        
        message = client.messages.create(
                        body="Hi, User You have break the following traffic rules "+challanBreaked+". Now you have to pay "+str(amount)+" Rs.</b> as Challan.",
                        from_='+13345183979',
                        to='++918867740558'
                    )
        return True
    except Exception as e:
        print('➡ main_app/utils.py:39 e:', e)
        return False