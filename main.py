#U JSON-u vazi samo ALT+SHIFT+F

from kivy.app import App
from kivy.lang import Builder  #Za povezivanje Python fajla i Kivy fajla
from kivy.uix.screenmanager import Screen, ScreenManager
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json
from datetime import datetime
import glob
from pathlib import Path
import random

Builder.load_file("design.kv")

class LoginScreen(Screen):
    def sign_up(self):
        #self je instanca trenutne klase, manager je deo screen-a, njegov property, a manager ima svoj atribute, a jedan od njih je i current i on dobija ime na koji ekran cemo da predjemo
        self.manager.current = "sign_up_screen"  #Ovo smo stavili da nam gadja novi ekran, pritiskom na dugme sign_up
    
    def login(self, uname, pword):
        with open("users.json", "r") as file:  #Ako ne stavim mod, podrazumeva se da je read, "r"
            users = json.load(file)
        
        if uname in users and users[uname]["password"] == pword:  #Proveravam da li je uneto ume u nasoj bazi i da li se sifra za to ime slaze sa unetom sifrom
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password!"  #Koristim self, njen atribut ids koji pristupa id Labele u kivy fajlu i moram metodu text, da bih mogao da pisem tu neki tekst i samo stavim = i tekst

    def get_password(self):
        self.manager.current = "forget_password_screen"


class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    def add_user(self, uname, pword):  #Ova dva parametra su textinput objekti, tj. nase vrednosti koje unosimo u input polja(proizvoljno ime)
        with open("users.json") as file:  #Otvorimo json file i ucitamo podatke u proizvoljnu varijablu(users)
            users = json.load(file)
        
        users[uname] = {"username": uname, "password": pword, "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  #Dodamo novog korisnika, uname je nase uneto ime, kao i pword(uneta sifra). A kljucevi su fiksni, zato su u navodnicima
        
        with open("users.json", "w") as file:  #Otvaram ponovo fajl, da snimim podatke, zato je mod w
            json.dump(users, file)  #Cuvam podatke u fajlu, a metoda dump zahteva dva parametra, prvi podaci, drugi ime fajla u kom ih snimam
        
        self.manager.current = "sign_up_screen_success"  #Da me prebaci kad pritisnem dugme SUBMIT na ovaj ekran, kao u liniji koda 15


class SignUpScreenSuccess(Screen):
    def change_window(self):
        #self je instanca ove klase, manager je property Screen-a, a njegov atribut je transition koji ima metodu direction
        self.manager.transition.direction = "right"  #Ovo mi pokazuje na koju stranu ce da se menja ekran. Po defaultu je levo, a sad ovde hocu desno
        self.manager.current = "login_screen"


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    
    def get_quote(self, feel):  #feel je zapravo nas tekst unet u input polje
        feel = feel.lower()  #Prebacim u mala slova nas unet tekst
        available_feelings = glob.glob("quotes/*txt")  #Glob sa metodom glob daje listu svih fajlova koji imaju ekstenziju .txt
        
        available_feelings = [Path(filename).stem for filename in available_feelings]  #Klasicna lista kompehenzije
        
        if feel in available_feelings:
            with open(f"quotes/{feel}.txt", encoding="utf-8") as file:  #Otavaram fajl, ali je feel nase uneto ime, u inputu
                quotes = file.readlines()  #Daje nam listu svih quotes-a
           
            self.ids.quote.text = random.choice(quotes)  #Stavili smo da random izbacuje quotes
        else:
            self.ids.quote.text = "Try another feeling!"


class ForgetPasswordScreen(Screen):
    def send_email(self, email):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"


#Klasa koja se sastoji od ova tri parametra i koja omogucava hover prilikom prelaska preko dugmeta
class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


#Ovo obavezno staviti, uvek je ovako, za sve aplikacije
class MainApp(App):
    def build(self):
        return RootWidget()


#Ovo obavezno staviti, da bi pokrenuli program
if __name__=="__main__":
    MainApp().run()


#Mogu da importujem Path iy modula pathlib i da koristim metodu stem da dobijem samo ime fajla, bez ekstenzije
#from pathlib import Path
#Path("quotes/sad.txt").stem  u navodnicima je putanja do fajla