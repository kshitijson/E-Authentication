import smtplib
import qrcode
from email.message import Message
import os
from os import path
import cv2
import math, random
from mailer import Mailer
from django.contrib.auth.models import User
import string
 

class AuthenticateUser:
    def __init__(self, name, mail):
        self.name = name
        self.mail = mail

    def generate_otp(self):
        def otp():
            digits = '0123456789'
            Otp = ''
            for i in range(4):
                Otp += digits[math.floor(random.random() * 10)]
            return Otp
        OTP = otp()
        
        try:
            msg = f"""Your Otp for this session is <b>{OTP}</b>
            
            Note: Don't share your otp with anybody"""
            mail = Mailer(email='e.authentication2002@gmail.com', password='rfdudovgzjqobcss')
            mail.send(receiver=self.mail, subject='Here is your OTP for Login', message=(msg))
            print('Mail Sent')
            return OTP
        except Exception as es:
            print('failed', es)

    def generate_QR(self):
        def salting():
            digits = '0123456789^!&#$%)(@_+=-=[]\';/.,<>?:"|}{#'
            salting_num = ''
            shuffled_digits = ''.join(random.sample(digits, len(digits)))
            salting_num += shuffled_digits[0:9]
            return salting_num
        salting_design = salting()

        dir = r'D:/QR/'
        path_qr = f"{dir}{self.name}.png"
        salted_name = f'{self.name}{salting_design}'
        if not os.path.isdir(dir):
            print('Creating directory')
            os.mkdir(dir)
            print('Directory created..... saving')
            qr_image = qrcode.make(salted_name)
            qr_image.save(path_qr)
            print(f'Your qr code is generated ate {dir}')
        else:
            qr_image = qrcode.make(salted_name)
            qr_image.save(path_qr)

        return salted_name

    def qr_name(self):
        return f"{self.name}.png"


class Decode:
    def __init__(self, file_loc):
        self.file_loc = file_loc

    def decode_qr(self):
        file = self.file_loc
        path = r"%s" % file
        detector = cv2.QRCodeDetector()
        content, point, s_qr = detector.detectAndDecode(cv2.imread(path))
        return content


class Change_passwd:
    def __init__(self, mail):
        self.mail = mail

    def send_passwd(self):
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")

        random.shuffle(characters)        
        password = []
        for i in range(0, 11):
            password.append(random.choice(characters))

        random.shuffle(password)
        passwd =  "".join(password)

        try:
            msg = f"""Your new temporary password is

            <b>{passwd}</b>
            
            Note: Change password immediately after login"""
            mail = Mailer(email='e.authentication2002@gmail.com', password='rfdudovgzjqobcss')
            mail.send(receiver=self.mail, subject='Temporory Password', message=(msg))
            print('Mail Sent')
            return passwd
        except Exception as es:
            print('failed', es)

