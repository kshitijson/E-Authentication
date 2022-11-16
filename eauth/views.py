from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from eauth.models import Signup
from eauth.models import FileUpload
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from validate_email_address import validate_email
from eauth import qr_otp
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
import os
import hashlib
import time


global loggedin            
loggedin = False

global usr_loggedin               # True after 1st phase of login
usr_loggedin = False

global authenticated              # True after 2nd phase of login
authenticated = False

global first_name                 # The first name of the user
first_name = ''

global usrname                    # The username of the user
usrname = ''

class Hash:
    def __init__(self, passwd):
        self.passwd = passwd
    
    def sha1(self):
        result = hashlib.sha1(self.passwd.encode())
        return result.hexdigest()



def home(request):
    return render(request, 'Home.html')


def signup(request):
    global usr_loggedin
    global authenticated

    if usr_loggedin == False and authenticated == False:
        if request.method == 'POST':
            name = request.POST.get('Full Name')
            usr = request.POST.get('Username')
            mobile = request.POST.get('Mobile Number')
            email = request.POST.get('Email Address')
            passphrase = request.POST.get('passphrase')
            gender = ''
            if request.POST.get('Male') == 'Male':
                gender = 'Male'
            else:
                gender = 'Female'
            dob = request.POST.get('dob')
            p = request.POST.get('pass')
            hashing = Hash(p)
            passwd = hashing.sha1()

            hashing_pp = Hash(passphrase)
            hashed_passphrase = hashing_pp.sha1()

            usr_check = Signup.objects.filter(username=usr)
            email_check = Signup.objects.filter(email=email)
            email_exists = validate_email(email)
            print(email_exists)

            if usr_check.exists():
                messages.warning(request, 'Username already exisits! Try again')
            elif email_check.exists():
                messages.warning(request, 'This Email Address is associated with different account! If it is your try logging in')
            elif not email:
                messages.warning(request, 'Email Address does not exist!! ❌')
            else:
                info = Signup(full_name=name, username=usr, mobile=mobile, email=email, gender=gender, dob=dob, password=passwd, passphrase=hashed_passphrase)
                info.save()
                messages.success(request, 'Registered Successfully!✅')

        return render(request, 'signup.html')
    
    return redirect('http://127.0.0.1:8000/Profile')


def login(request):
    global usr_loggedin
    global first_name
    global usrname
    global authenticated
    first_name = ''

    if usr_loggedin == False and authenticated == False:
        if request.method == 'POST':
            usrname = ''
            login.usr = request.POST.get('input')
            p = request.POST.get('passwd')
            result = Hash(p)
            login.passwd = result.sha1()
            usr_name = login.usr
            print(login.usr)
            print(login.passwd)
            if '@' in usr_name:       # If @ present in string than it is email address
                username = False      # Not  a Username
                login_usr = Signup.objects.filter(email=login.usr, password=login.passwd)                                                # add password field in signup of models
            else:
                username = True       # Is a Username
                usrname = usr_name
                login_usr = Signup.objects.filter(username=login.usr, password=login.passwd)


            if login_usr.exists() and username == False:     # If usrname and password are correct but it is an email
                print('Hello')
                for e in Signup.objects.filter(email=login.usr):
                    names = e.full_name
                    mail = e.email
                    usrname = e.username

                for n in names:
                    if n != " ":
                        first_name += n
                    else:
                        break
                
                dir = f'D:/QR/{first_name}.png'
                dir_corrected = r"%s" % dir

                if os.path.exists(dir_corrected):
                    os.remove(dir_corrected)

                two_factor = qr_otp.AuthenticateUser(name=first_name, mail=mail)
                login.qr = two_factor.generate_QR()
                login.ottp = two_factor.generate_otp()
                usr_loggedin = True
                return redirect('Login/2-Factor-Authentication')
                # redirect('Login/2-Factor-Authentication')


            elif login_usr.exists() and username == True:    # If usrname and password are correct but it is a username

                for e in Signup.objects.filter(username=login.usr):
                    names = e.full_name
                    mail = e.email
                
                for n in names:
                    if n != " ":
                        first_name += n
                    else:
                        break
                
                print(first_name, "Username is true")
                dir = f'D:/QR/{first_name}.png'
                dir_corrected = r"%s" % dir

                if os.path.exists(dir_corrected):
                    os.remove(dir_corrected)

                two_factor = qr_otp.AuthenticateUser(name=first_name, mail=mail)
                login.qr = two_factor.generate_QR()
                login.ottp = two_factor.generate_otp()
                usr_loggedin = True
                return redirect('Login/2-Factor-Authentication')

            else:
                messages.warning(request, "Invalid Credentials")

        return render(request, 'login.html')

    return redirect('http://127.0.0.1:8000/Profile')


def two_factor(request):
    global usr_loggedin
    global first_name
    global authenticated

    if usr_loggedin:
        if request.method == 'POST':
            o_t_p = request.POST.get('otp')
            qr_code = request.FILES['document']
            files = FileUpload.objects.create(file=qr_code)
            files.save()

            username = login.usr
            passwrd = login.passwd
            name = first_name
            file_location = f'C:/Users/ASUS/Python Projects/Authentication/media/{name}.png'
            try:
                dec_qr = qr_otp.Decode(file_location)
                decoded_content = dec_qr.decode_qr()
            except Exception as es:
                messages.warning(request, "Invalid Qr Code!❌")
                usr_loggedin = False                                   # set it false so we can access login page
                
                path_file = f'C:/Users/ASUS/Python Projects/Authentication/media/{first_name}.png'
                path_file_corrected = r"%s" % path_file
                if os.path.exists(path_file_corrected):                           # delete qr file from media folder
                    os.remove(path_file_corrected)

                time.sleep(2)
                return redirect("http://127.0.0.1:8000/Login")
                
            if login.ottp == o_t_p and login.qr == decoded_content:    #Check if the otp matches and the qr aswell
                authenticated = True
                return redirect('http://127.0.0.1:8000/Profile')                         
            else:                                                      # iF INVALID qR OR OTP
                if o_t_p != login.ottp:
                    messages.warning(request, "Invalid OTP!❌")
                elif login.qr == decoded_content:
                    messages.warning(request, "Invalid Qr Code!❌")
                usr_loggedin = False                                   # set it false so we can access login page
                
                path_file = f'C:/Users/ASUS/Python Projects/Authentication/media/{first_name}.png'
                path_file_corrected = r"%s" % path_file
                if os.path.exists(path_file_corrected):                           # delete qr file from media folder
                    os.remove(path_file_corrected)

                time.sleep(2)
                return redirect("http://127.0.0.1:8000/Login")                    # return to login page
        
        return render(request, 'two_factor_auth.html')
    else:
        return redirect("http://127.0.0.1:8000/Login")
    

def profile(request):
    global usr_loggedin
    global first_name
    global authenticated
    global usrname


    if usr_loggedin and authenticated:
        path_file = f'C:/Users/ASUS/Python Projects/Authentication/media/{first_name}.png'
        path_file_corrected = r"%s" % path_file
        if os.path.exists(path_file_corrected):
            os.remove(path_file_corrected)

        print(usrname)
        context = {'name': first_name, 'username': usrname}
        return render(request, 'index.html', context)     
    else:
        return redirect('http://127.0.0.1:8000/Login')


def logoutusr(request):
    global usr_loggedin
    global authenticated
    global usrname
    global first_name

    usr_loggedin = False
    authenticated = False
    usrname = ''
    first_name = ''

    return redirect('http://127.0.0.1:8000/Login')


def ch_pass(request):
    global usr_loggedin
    global authenticated
    global usrname    

    if usr_loggedin and authenticated:
        if request.method == 'POST':
            old_passwd = request.POST.get('oldpassword')
            new_passwd = request.POST.get('password')

            res1 = Hash(new_passwd)
            hashed_new_passwd = res1.sha1()
            res2 = Hash(old_passwd)
            hashed_old_passwd = res2.sha1()

            for e in Signup.objects.filter(username=usrname):
                old_dbpasswd = e.password


            if old_dbpasswd != hashed_old_passwd:
                messages.warning(request, 'Invalid Old password')
                print('first if executed')
            if hashed_old_passwd == hashed_new_passwd:
                messages.warning(request, 'Old password and New password must not be same')
                print('Second if executed')
            if old_dbpasswd == hashed_old_passwd and hashed_old_passwd != hashed_new_passwd:
                try:
                    passwd = Signup.objects.get(username=usrname)
                    passwd.password = hashed_new_passwd
                    passwd.save()
                    messages.success(request, 'Password Changed Successfully')
                    print(old_dbpasswd)
                    print(hashed_old_passwd)
                    print(hashed_new_passwd)
                except Exception as es:
                    print(es)

        context = {'username': usrname}
        return render(request, 'change_pass.html', context)
    else:
        return redirect('http://127.0.0.1:8000/Home')


def ch_pass_unauthenticated(request):
    global usr_loggedin
    global authenticated

    if not usr_loggedin and not authenticated:
        if request.method == 'POST':
            email = request.POST.get("email")
            pp = Hash(request.POST.get('passphrase'))
            passphrase = pp.sha1()

            usr = Signup.objects.filter(email=email, passphrase=passphrase)

            if usr.exists():
                print("Exists")
                generate_passwd = qr_otp.Change_passwd(mail=email)
                new_passwd = Hash(generate_passwd.send_passwd())
                hashed_new_passwd = new_passwd.sha1()

                passwd = Signup.objects.get(email=email)
                passwd.password = hashed_new_passwd
                passwd.save()
                messages.success(request, 'Password Generated and Emailed Successfully✅')
            else:
                messages.warning(request, 'Invalid Email Address or Passphrase❌')

        return render(request, 'change_pass_notloggedin.html')
    else:
        return redirect('http://127.0.0.1:8000/Profile')

def contact_us(request):
    return render(request, 'contact.html')
