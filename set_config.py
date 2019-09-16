#first time setup, also happens if directory is empty, or invalidaaaa
import os
import yaml
from ftplib import FTP
from keyboard import is_pressed # using module keyboard
from tkinter import messagebox, Label, Button, FALSE, Tk, Entry, Checkbutton, BooleanVar, StringVar
from progress.spinner import Spinner
from tkinter.filedialog import askdirectory
class set_config:
    def __init__(self, config_path):
        self.config_path = config_path
    window = Tk()
    def first(self):
        with open(self.config_path + '/path.yaml', 'w') as stream:
            result = messagebox.askyesno("Defaults", "Would you like to use defaults")
            #user navigates to desired directory
            if result is False:
                directory = askdirectory();
                yaml.dump({'File': directory}, stream)
            #directory defaults to creating a subdirectory of current folder called DragonFieldTest
            else:
                directory_default = self.config_path[:-6]#default data directory
                directory_default = directory_default + "FieldTest"
                if not(os.path.exists(directory_default)):
                    os.mkdir(directory_default)
                yaml.dump({'File': directory_default}, stream)
    def save_login(self,username, password):
        #save data if checkboxes are checked
        with open(self.config_path + "/login.yaml", 'w') as stream:
            yaml.dump({'Username': username.get()}, stream)
            yaml.dump({"Password": password.get()}, stream)
        #window.quit()
    #creates data entry fields in gui and collects user info, such as username, pass and whether to save the info
    def user_info(self):
        #gui stuff
        self.window.resizable(width=FALSE, height=FALSE)
        self.window.title("Log-In")
        self.window.geometry("200x150")
        #vars    
        username = StringVar()
        password = StringVar()
        #Creating the username & password entry boxes
        username_text = Label(self.window, text="Username:")
        username_entry = Entry(self.window, textvariable = username)
        password_text = Label(self.window, text="Password:")
        password_entry = Entry(self.window, show="*", textvariable = password)

        #attempt to login button

        attempt_login = Button(self.window, text="Save", command= lambda: self.save_login(username, password))

        username_text.pack()
        username_entry.pack()
        password_text.pack()
        password_entry.pack()
        attempt_login.pack()
        #Main Starter
        self.window.mainloop()
    def setup(self):
        if not(os.path.exists("C:/Dragon")):
            os.mkdir("C:/Dragon")
        if not(os.path.exists(self.config_path)):
            os.mkdir(self.config_path)
        if not(os.path.exists(self.config_path +"/path.yaml")):
            self.first()
        if not (os.path.exists(self.config_path + "/login.yaml")):
            self.user_info()
        else: 
            result = messagebox.askyesno("ChangeLogin", "Would you like to change login info?")
            #user navigates to desired directory
            if result is True:
                self.user_info()
                
        with open(self.config_path + '/path.yaml', 'r') as stream:
            path_info = yaml.safe_load(stream)
            #make sure the file is not empty
            if(path_info == None):
                self.first()
        #if the login yaml doc doesnt exist, setup gui and take in user info
        with open(self.config_path + "/login.yaml", 'r') as stream:
            login_info = yaml.safe_load(stream)
            #if any info is missing display login gui
            if(login_info == None):# or login_info.get("Password") == None or login_info.get("Username") == None):
                self.user_info_gui_setup(username, password)
                self.user_info(username, password)