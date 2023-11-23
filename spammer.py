import smtplib

toadrs = input("Enter victim's email:\n")
frmadrs = input("Enter your email:\n")

message = input("Enter your message:\n")

with smtplib.SMTP('smtp.gmail.com', '587') as smtpserver:
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    smtpserver.login('xyz@gmail.com', 'your app pswd')     # in the first '' type your email id (from which mail id your are sending the spams) and in the second '' type your app password.

    for i in range(int(input("Number of emails:\n"))):
        smtpserver.sendmail(frmadrs, toadrs, message)
        print(i)

print("Spam successful!")
input("Press any key to close.")
