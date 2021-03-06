
import os
import platform
import subprocess
import json 
import hashlib
from vulnerability import Vulnerability
from tkinter import *
from tkinter import ttk
from graphical import CreationView
from graphical import GetCredentials
from graphical import CreateUser

class Controller: 
    """
    Controller of the Model View Controller

    ...

    Attributes
    ----------
    model: Vulnerability
        a variable to save all information about the Vulnerability

    username: str
        username is required for login

    password: str
        password is required for login

    msg: str
        msg is required for the login View

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes

    gui_loop(self)
        the main loop of the calculator application, the root is a Tk Window

    start(self)
        authentication that is required to get access to the program

    check_auth_gui(self)
        is checking if a auth.json (contains userdata) is in the template folder. if true
            the programm will start with the login window otherwise with the sign up window

    set_user(self, user):
        setting the current user

    set_password(self, password):
        setting the current password

    set_msg(self, msg):
        setting the message that is required 

    print_json(self)
        creates an .json file. the name of the file is the same as for model.get_name().    
            the file is saved inside the output folder.

    print_txt(self)
        creates an .json file. the name of the file is the same as for model.get_name().    
            the file is saved inside the output folder.

    get_vector(self) -> str
        return the CVSS 3.1 Vector

    set_metric(self, base_string, value=None)
        is changing the values of the vector. if the value is None (default) the  program is 
            got the base score from the view and is setting it for the model. otherwise
            its just a single metric which sets the value for the base_string 

    get_metric(self, env): -> str
        returns the value of the selected metric BASE, ENV, TEMP

    get_base_score(self):
        returns the base_score

    get_env_score(self):
        return the environmental score

    get_temp_score(self):
        return the temp  score

    set_asset(self):
        set the name of the asset

    set_vul(self):
        set the name  of the vulnerability

    get_user(self):
        get the name of the user

    get_password(self):
        get the name of the password
    """
    def __init__(self): 
        self._model = Vulnerability()
        self.username = ""
        self.password = ""
        self.msg = ""
        self.check_auth = False

    def gui_loop(self): 
        root = Tk()
        #get_credentials(root, self)
        root.resizable(False,False)
        root.title('cvsslator')
        self._view = CreationView(root, self)
        root.mainloop()

    def start(self):
        self.msg = "LOGIN"
        self.check_auth_gui()

    def check_auth_gui(self):
    
        if os.path.isfile('../templates/auth.json'):

            GetCredentials(self, self.msg)
            
            if self.username == "" and self.password == "":
                 return False
            else:
                hash_object = hashlib.sha256(self.password.encode('ascii'))
                hash_password = str(hash_object.hexdigest())



                with open('../templates/auth.json') as auth:
                   credentials = json.load(auth)


                if self.username == credentials['user'] and hash_password == credentials['password']:
                        self.username = ""
                        self.password = ""
                        self.gui_loop()
                        return True

                else:
                        self.username = ""
                        self.password = ""
                        self.msg = "Unknown Combination!"
                        self.check_auth_gui()
                        return False
        else:

            CreateUser(self)

            if self.check_auth:

                hash_object = hashlib.sha256(self.password.encode('ascii'))
                hash_password = str(hash_object.hexdigest())

                credentials = {
                    'user': self.username,
                    'password': hash_password

                }

                with open('../templates/auth.json', 'w') as auth:
                    json.dump(credentials, auth)
            
                self.username = ""
                self.password = ""
            
                self.gui_loop()
                return "set"
            else: 
                return False
    
    def set_user(self, username):
        self.username = username

    def set_password(self, password):
        self.password = password
    
    def set_msg(self, msg):
        self.msg = msg

    def print_json(self): 
        with open('../templates/template_output_json.json') as out:
            try:
            	JSON_OUT = json.load(out)
            except json.decoder.JSONDecodeError:
                return False
        
        JSON_OUT['asset_name'] = self._model.get_asset_name()
        JSON_OUT['vuln_name'] = self._model.get_vulnerability_name()
        JSON_OUT['vektor'] = self._model.get_vector()
        JSON_OUT['base_score'] = self._model.get_base_score()
        JSON_OUT['temp_score'] = self._model.get_temp_score()
        JSON_OUT['env_score'] = self._model.get_env_score()
        JSON_OUT['total_score'] = self._model.get_total_score()

        if self._model.get_asset_name() != "N/D":
            create_name = '../output/' + self._model.get_asset_name() + '_output.json'
        else:
            create_name = "../output/unknown_output.json"
        
        with open(create_name, 'w') as out2:
            out2.write(json.dumps(JSON_OUT, indent=4))

        return True

    def print_txt(self): 
        with open('../templates/template_output_txt.txt' , 'r') as file:
            TXT_OUT = file.read()
            TXT_OUT = TXT_OUT.replace('$asset_name$', self._model.get_asset_name())
            TXT_OUT = TXT_OUT.replace('$vul_name$', self._model.get_vulnerability_name())
            TXT_OUT = TXT_OUT.replace('$vektor$', str(self._model.get_vector()))
            TXT_OUT = TXT_OUT.replace('$base_score$', str(self._model.get_base_score()))
            TXT_OUT = TXT_OUT.replace('$temp_score$', str(self._model.get_temp_score()))
            TXT_OUT = TXT_OUT.replace('$env_score$', str(self._model.get_env_score()))
            TXT_OUT = TXT_OUT.replace('$total_score$', str(self._model.get_total_score()))



            if self._model.get_asset_name() != "N/D":
                create_name = '../output/' + self._model.get_asset_name() + '_output.txt'
            else: 
                create_name = "../output/unknown_output.txt"


            with open(create_name , 'w') as output:
                output.write(TXT_OUT)

    def get_vector(self): 
        return self._model.get_vector()

    def set_metric(self, base_string, value=None):
        if value == None:
            self._model.set_vector(base_string)
        else: 
            self._model.set_metric(base_string, value)

    def get_metric(self, type): 
        if type == "BASE": 
            return self._model.get_base_vector()
        elif type=="TEMP": 
            return self._model.get_temp_vector()
        elif type=="ENV": 
            return self._model.get_env_vector()
        else: 
            pass

    def get_base_score(self): 
        return self._model.get_base_score()

    def get_env_score(self): 
        return self._model.get_env_score()

    def get_temp_score(self): 
        return self._model.get_temp_score()

    def set_vul(self, value): 
        if value == "":
            self._model.set_asset_name("N/D")
        else:
            self._model.set_vulnerability_name(value)
    
    def set_asset(self, value):
        if value == "":
            self._model.set_asset_name("N/D")
        else:
            self._model.set_asset_name(value)
    
    def get_user(self):
        return self.username
    
    def get_password(self):
        return self.password

