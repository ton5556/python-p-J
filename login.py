from stdiomask import getpass
import hashlib
import os
import webbrowser
import win32com.client as wincl

speak = wincl.Dispatch("SAPI.SpVoice")

clear = lambda: os.system('cls')


def main():
    clear()
    print("MAIN MENU")
    speak.Speak("MAIN MENU")
    print("---------")
    print()
    print("1 - Register")
    speak.Speak("choose 1 to Register")
    print("2 - Login")
    speak.Speak("choose 2 to Login")
    print()
    while True:
        print()
        userChoice = input("Choose An Option: ")
        if userChoice in ['1', '2']:
            break
    if userChoice == '1':
        Register()
        speak.Speak("choose 1 Register")
    else:
        Login()
        speak.Speak("choose 2 to Login")

def Register():
    clear()
    print("REGISTER")
    print("--------")
    speak.Speak("to Register")
    print()
    while True:
        speak.Speak("Your Name")
        userName = input("Enter Your Name: ").title()
        if userName != '':
            break
    userName = sanitizeName(userName)
    if userAlreadyExist(userName):
        displayUserAlreadyExistMessage()
    else:
        while True:
            speak.Speak("Your Password")
            userPassword = getpass("Enter Your Password: ")
            if userPassword != '':
                break
        while True:
            speak.Speak("Confirm Your Password")
            confirmPassword = getpass("Confirm Your Password: ")

            if confirmPassword == userPassword:
                break
            else:
                print("Passwords Don't Match")
                speak.Speak("ลืมรหัสเเล้ว เเค่นี้จะลืมเขาได้ยังไง")
                print()
        if userAlreadyExist(userName, userPassword):
            while True:
                print()
                error = input("You Are Already Registered.\n\nPress (T) To Try Again:\nPress (L) To Login: ").lower()
                if error == 't':
                    Register()
                    break
                elif error == 'l':
                    Login()
                    break
        addUserInfo([userName, hash_password(userPassword)])

        print()
        print("Registered!")

def Login():
    clear()
    print("LOGIN")
    speak.Speak("LOGIN")
    print("-----")
    print()
    usersInfo = {}
    with open('userinfo.txt', 'r') as file:
        for line in file:
            line = line.split()
            usersInfo.update({line[0]: line[1]})

    while True:
        speak.Speak("Enter Your Name")
        userName = input("Enter Your Name: ").title()
        userName = sanitizeName(userName)
        if userName not in usersInfo:
            print("You Are Not Registered")
            print()
        else:
            break
    while True:
        speak.Speak("Enter Your Password")
        userPassword = getpass("Enter Your Password: ")

        if not check_password_hash(userPassword, usersInfo[userName]):
            print("Incorrect Password")
            speak.Speak(" Incorrect Password")
            print()
        else:
            break
    print()
    speak.Speak("We are taking you to the website")
    webbrowser.open('http://net-informations.com', new=1)
    print("Logged In!")



def addUserInfo(userInfo: list):
    with open('userInfo.txt', 'a') as file:
        for info in userInfo:
            file.write(info)
            file.write(' ')
        file.write('\n')

def userAlreadyExist(userName, userPassword=None):
    if userPassword == None:
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                if line[0] == userName:
                    return True
        return False
    else:
        userPassword = hash_password(userPassword)
        usersInfo = {}
        with open('userInfo.txt', 'r') as file:
            for line in file:
                line = line.split()
                if line[0] == userName and line[1] == userPassword:
                    usersInfo.update({line[0]: line[1]})
        if usersInfo == {}:
            return False
        return usersInfo[userName] == userPassword

def displayUserAlreadyExistMessage():
    while True:
        print()
        error = input("You Are Already Registered.\n\nPress (T) To Try Again:\nPress (L) To Login: ").lower()
        if error == 't':
            Register()
            break
        elif error == 'l':
            Login()
            break

def sanitizeName(userName):
    userName = userName.split()
    userName = '-'.join(userName)
    return userName

def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password_hash(password, hash):
    return hash_password(password) == hash


main()