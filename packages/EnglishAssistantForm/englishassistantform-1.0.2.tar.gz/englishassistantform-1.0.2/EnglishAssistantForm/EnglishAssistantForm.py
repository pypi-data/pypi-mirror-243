import customtkinter as ctk
from tkinter import *
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfile
from awesometkinter.bidirender import render_text
from PIL import Image
import os
import requests
import re
import json
import random

from EnglishAssistantCore import Core as SC # use it from pypi



## exe app
## https://github.com/TomSchimansky/CustomTkinter/wiki/Packaging
class Splash(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:

        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        
        super().__init__(*args, **kwargs)

        self.title("Splash")

        self.folder_path = os.path.join(os.path.dirname(__file__))
        self.file_name = os.path.join(self.folder_path, 'SplashScreen.png')
        self.img = Image.open(self.file_name)
        Hi = self.img.height
        Wi = self.img.width

        YLoc = str((self.winfo_screenheight()//2)-(Hi//2))
        XLoc = str((self.winfo_screenwidth()//2)-(Wi//2))
        self.geometry(str(Wi)+"x"+str(Hi)+"+"+XLoc+"+"+YLoc)


        self.ctk_img = ctk.CTkImage(self.img,size=[Wi , Hi])
        self.label = ctk.CTkLabel(master=self ,image=self.ctk_img, text="").place(x=0, y=0)


        self.overrideredirect(True)
        self.wm_attributes('-topmost')
        self.config(cursor="none")

        
        
        ## required to make window show before the program gets to the mainloop
        self.update_idletasks()
        self.update()



class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Pronunciation")
        self.add("Speaker")
        self.add("Writing")
        self.add("Listener")

        # Add widgets on tabs
        # Tab1 # Row 0
        self.button1 = ctk.CTkButton(master=self.tab("Pronunciation"),text="⏪",font=('Consolas bold',22),width=56)
        self.button1.grid(row=0, column=0,columnspan=2, padx=(10,10), pady=(20, 20), sticky="nsew")
        self.button2 = ctk.CTkButton(master=self.tab("Pronunciation"),text="▶️",font=('Consolas bold',22),width=56)
        self.button2.grid(row=0, column=2,columnspan=2,padx=(10,10), pady=(20, 20), sticky="nsew")
        self.button3 = ctk.CTkButton(master=self.tab("Pronunciation"),text="⏩",font=('Consolas bold',22),width=56)
        self.button3.grid(row=0, column=4,columnspan=2,padx=(10,10), pady=(20, 20), sticky="nsew")

        # Tab1 # Row 1,2,3,4
        self.label1 = ctk.CTkLabel(master=self.tab("Pronunciation"), text="Persian",font=('Times New Roman bold',40))
        self.label1.grid(row=1, column=0,columnspan=6, padx=(10,10), pady=(20, 20), sticky="w")
        self.label2 = ctk.CTkLabel(master=self.tab("Pronunciation"), text="/Pronunciation/",font=('Consolas bold',20))
        self.label2.grid(row=2, column=0,columnspan=6, padx=(10,10), pady=(20, 20), sticky="w")
        self.label3 = ctk.CTkLabel(master=self.tab("Pronunciation"), text="Noun",font=('Consolas bold',20))
        self.label3.grid(row=3, column=0,columnspan=6, padx=(10,10), pady=(20, 20), sticky="w")
        self.label4 = ctk.CTkLabel(master=self.tab("Pronunciation"), text=render_text("فارسی"),font=('Homa bold',20),justify=ctk.RIGHT)
        self.label4.grid(row=4, column=0,columnspan=6, padx=(10,10), pady=(20, 20), sticky="e")
        
        # Tab1 # Row 5
        self.combo1 = ctk.CTkOptionMenu(master=self.tab("Pronunciation"),font=('Times New Roman bold',20),width=20,height=60,dropdown_font=('Times New Roman',12),dynamic_resizing=True)
        self.combo1.grid(row=5, column=0,columnspan=6,padx=(10,10), pady=(30, 30), sticky="nsew")
        
        # Tab1 # Row 6
        self.button4 = ctk.CTkButton(master=self.tab("Pronunciation"),text="+",font=('Consolas bold',22),width=35)
        self.button4.grid(row=6, column=0,columnspan=1,padx=(10,10),pady=(20, 20), sticky="nsew")
        self.button5 = ctk.CTkButton(master=self.tab("Pronunciation"),text="-",font=('Consolas bold',22),width=35)
        self.button5.grid(row=6, column=1,columnspan=1,padx=(10,10), pady=(20, 20), sticky="nsew")
        self.button6 = ctk.CTkButton(master=self.tab("Pronunciation"),text="Import Data Base",font=('Consolas bold',9),width=56)
        self.button6.grid(row=6, column=2,columnspan=1,padx=(10,10), pady=(20, 20), sticky="nsew")
        self.button7 = ctk.CTkButton(master=self.tab("Pronunciation"),text="Export Data Base",font=('Consolas bold',9),width=56)
        self.button7.grid(row=6, column=4,columnspan=1,padx=(10,10), pady=(20, 20), sticky="nsew")

        # Tab1 # Row 7
        self.text1 = ctk.CTkTextbox(master=self.tab("Pronunciation"),font=('Consolas bold',25))
        self.text1.grid(row=7, column=0,columnspan=6, padx=(10,10), pady=(20, 15), sticky="w")
        self.text1.insert("0.0", "")



        # Tab2 # Row 0
        self.button21 = ctk.CTkButton(master=self.tab("Speaker"),text="Rand. String Topic",font=('Consolas bold',9),width=56)
        self.button21.grid(row=0, column=0,columnspan=2, padx=(10,10), pady=(20, 20), sticky="nsew")
        self.button22 = ctk.CTkButton(master=self.tab("Speaker"),text="Rand. Image Topic",font=('Consolas bold',9),width=56)
        self.button22.grid(row=0, column=2,columnspan=2,padx=(10,10), pady=(20, 20), sticky="nsew")
        self.button23 = ctk.CTkButton(master=self.tab("Speaker"),text="Desired Paraghraph",font=('Consolas bold',8.5),width=56)
        self.button23.grid(row=0, column=4,columnspan=2,padx=(10,10), pady=(20, 20), sticky="nsew")

        # Tab2 # Row 1
        self.label21 = ctk.CTkLabel(master=self.tab("Speaker"), text="",font=('Times New Roman bold',40))
        self.label21.grid(row=1, column=0,columnspan=6, padx=(10,10), pady=(20, 20), sticky="nsew")

        # Tab2 # Row 2
        self.label22 = ctk.CTkLabel(master=self.tab("Speaker"), text="",font=('Consolas bold',15))
        self.label22.grid(row=2, column=0,columnspan=6, padx=(10,10), pady=(20, 20), sticky="nsew")

        # Tab2 # Row 3
        self.slider1 = ctk.CTkSlider(master=self.tab("Speaker"),width=100)
        self.slider1.grid(row=3, column=0,columnspan=6,padx=(10,10), pady=(20, 20), sticky="nsew")

        # Tab2 # Row 4
        self.text21 = ctk.CTkTextbox(master=self.tab("Speaker"),font=('Consolas bold',12), state="disabled")
        self.text21.grid(row=4, column=0,columnspan=6, padx=(10,10), pady=(20, 15), sticky="nsew")
        self.text21.insert("0.0", "")

        # Tab2 # Row 5
        self.button24 = ctk.CTkButton(master=self.tab("Speaker"),text="Play(▶️)",font=('Consolas bold',11),width=56)
        self.button24.grid(row=5, column=0,columnspan=2, padx=(10,10), pady=(20, 20), sticky="nsew")
        self.button25 = ctk.CTkButton(master=self.tab("Speaker"),text="Rec (💾)",font=('Consolas bold',11),width=56) # 💾 ●
        self.button25.grid(row=5, column=2,columnspan=2,padx=(10,10), pady=(20, 20), sticky="nsew")
        self.button26 = ctk.CTkButton(master=self.tab("Speaker"),text="en",font=('Consolas bold',11),width=56)
        self.button26.grid(row=5, column=4,columnspan=2,padx=(10,10), pady=(20, 20), sticky="nsew")











        # Tab3 # 
        self.label = ctk.CTkLabel(master=self.tab("Writing"),text="The Writing module is not complete.")
        self.label.grid(row=0, column=0, padx=(10,10), pady=(20,20))
        
        # Tab4 # 
        self.label = ctk.CTkLabel(master=self.tab("Listener"),text="The Listener module is not complete.")
        self.label.grid(row=0, column=0, padx=(10,10), pady=(20,20))



class App(ctk.CTk):

    def __init__(self) -> None:
        ctk.set_appearance_mode("Dark") 
        ctk.set_default_color_theme("dark-blue")

        
        # Initialize Objects
        super().__init__()
        self.resizable(0,0)
        self.withdraw()
        self.splash = Splash(self)

        # Local Variables
        Width = 390 ;
        Height = 690 ;

        

        self.folder_path = os.path.join(os.path.dirname(__file__))
        self.title("English Language Application")   
        self.geometry(str(Width)+"x"+str(Height)+"+0+0")
        self.iconbitmap(self.get_software_icon())
        
        # Local Variables (Data base and passable varibles)
        self.Words = self.read_file_in_list(os.path.join(self.folder_path, 'Data.db'))
        self.ImageDataBase = json.load(open(os.path.join(self.folder_path+"/topic_src", 'DataDict.json')))
        self.TopicDataBase = json.load(open(os.path.join(self.folder_path+"/topic_src", 'DataDict.json')))
        self.combo_bind_var = None ;
        self.slider_bind_var = None ;
        

        # Tabs
        self.tab_view = MyTabView(master=self,width=Width-30,height=Height-15)
        self.tab_view.grid(row=0, column=0, padx=(15,15), pady=(0,15))

        # Apply Commands
        ## Tab 1
        self.tab_view.button1.configure(command=self.backward)
        self.tab_view.button2.configure(command=self.implementation)
        self.tab_view.button3.configure(command=self.forward)
        self.tab_view.combo1.configure(command=self.combobox_callback)
        self.tab_view.button4.configure(command=self.add_word_to_list)
        self.tab_view.button5.configure(command=self.remove_word_from_list)

        self.tab_view.button6.configure(command=self.import_data_base)
        self.tab_view.button7.configure(command=self.export_data_base)
        self.tab_view.text1.configure(width=Width-30-30,height=35)

        ## Tab 2
        self.tab_view.button21.configure(command=self.random_topic_text_sentences)
        self.tab_view.button22.configure(command=self.random_topic_image_sentences)
        self.tab_view.button23.configure(command=self.desired_topic_sentences)

        self.tab_view.label21.configure(image = self.file_name_to_ctkimage('Blank.png'))

        self.tab_view.label22.configure(text = "Blank")

        self.slider_bind_var = IntVar(value=120)
        self.tab_view.slider1.configure(from_=120, to=220, variable=self.slider_bind_var,command=self.change_rate)
        
        self.tab_view.text21.configure(width=Width-30-30,height=140)
        
        self.tab_view.button24.configure(command=self.implementation_sentences)
        self.tab_view.button25.configure(command=self.record_sentences)
        self.tab_view.button26.configure(command=self.do_nothing)



        # Binding and Update
        self.bind_and_update()

        ## schedule closing the splash window after a delay
        self.after(0, self.destroy_splash_show_main_window)





    ## Constructors
    def get_software_icon(self):
        file_name = 'icon.ico'
        return os.path.join(self.folder_path, file_name)
    
    def destroy_splash_show_main_window(self):
        ## show window again
        self.wm_deiconify()
        # self.deiconify()

        ## finished loading so destroy splash
        self.splash.destroy()

    def get_image_by_name(self,FileName):
        return os.path.join(self.folder_path+"\topic_src", FileName)
    
    ## Methods
    def read_file_in_list(self,full_name):
        lines = []
        with open(full_name, 'r') as file:
            for line in file:
                line = line.strip()
                if len(line) != 0 :
                    lines.append(line)
        return lines

    def write_list_in_file(self):
        file_name = 'Data.db'
        full_name = os.path.join(self.folder_path, file_name)
        with open(full_name, "w") as file:
            file.writelines(line + "\n" for line in self.Words)
    
    def internet_connection(self):
        try:
            response = requests.get("https://www.google.com", timeout=1000)
            return True
        except requests.ConnectionError:
            return False   
    
    def Binding(self,Obj,List,Method): # Very Important Event
        BindVar = StringVar()
            
        if len(List) == 0:
            BindVar.set("None")
            Obj.configure(values = [],variable = BindVar)
        else :
            BindVar.set(List[-1])
            Obj.configure(values = List,variable = BindVar)

        BindVar.trace('w', Method)
        
        return BindVar
    
    def bind_and_update(self):
        # Binding
        self.combo_bind_var = self.Binding(self.tab_view.combo1,self.Words,self.update_values)
        
        # Updates value to show
        self.update_values()

    def update_values(self,*args):
        _core = SC.Core()
        # Label 1
        self.tab_view.label1.configure(text = self.combo_bind_var.get())
        
        # Label 2
        _pron = _core.find_pronunc(list(filter(None, re.split(r'\s|\.|,', self.combo_bind_var.get()))))
        self.tab_view.label2.configure(text = _pron)

        # Label 3
        _tag = _core.find_tag_spacy(self.combo_bind_var.get())
        _expo = _core.tag_translator_spacy(_tag)
        self.tab_view.label3.configure(text = _expo)

        # Label 4
        if self.internet_connection():
            _core.set_translator_lang()
            _trans = _core.translate_action(self.combo_bind_var.get())
            self.tab_view.label4.configure(text = _trans)
        else :
            self.tab_view.label4.configure(text = "")

    def file_name_to_ctkimage(self,FileName):
        file_name = os.path.join(self.folder_path+"\\topic_src",FileName )
        img_tab1 = Image.open(file_name)
        return ctk.CTkImage(img_tab1,size=[125 , 75])


    ## Events
    def add_word_to_list(self):
        new_word = self.tab_view.text1.get("1.0","end-1c")
        is_unique = not [word for word in self.Words if new_word == word]
        if new_word.replace(" ", "").isalpha() and is_unique: # and not repeated
            self.Words.append(new_word)
            self.tab_view.combo1.configure(values=self.Words)
            if len(self.Words) > 0 : self.tab_view.combo1.set(self.Words[-1])
            self.write_list_in_file()
        self.tab_view.text1.delete("1.0", "end")

    def remove_word_from_list(self):
        if len(self.Words) != 0 :
            index_word = self.tab_view.combo1.get()

            list_words = self.Words
            index_dict = {word: idx for idx, word in enumerate(list_words)}

            removed_index = index_dict[index_word] ## Will removed
            list_words.remove(index_word)

            self.Words = list_words
            self.tab_view.combo1.configure(values=self.Words)

            self.tab_view.combo1.set("None") if len(self.Words) == 0 else self.tab_view.combo1.set(self.Words[removed_index-1])
            self.write_list_in_file()

    def implementation(self):
        _core = SC.Core()
        _core.speak(self.combo_bind_var.get())
    
    def implementation_sentences(self):
        _core = SC.Core()
        _core.set_rate(round(self.slider_bind_var.get()))
        _core.speak(self.tab_view.text21.get("1.0","end-1c"))

    def record_sentences(self):

        try:
            f = asksaveasfilename(initialfile = 'Output.mp3', defaultextension=".mp3",filetypes=[("MPEG-2 Audio Layer III","*.mp3")])
            
            if len(f).__eq__(0) : # asksaveasfile return `None` if dialog closed with "cancel".
                return
            
            file_name, file_extension = os.path.splitext(f)
            stringlist = list(filter(None, re.split(r'\s|\.|,', self.tab_view.text21.get("1.0","end-1c"))))

            if (file_extension.lower().__eq__(".mp3")) and ( not(len(stringlist).__eq__(int(0))) ) :
                _core = SC.Core()
                _core.set_rate(round(self.slider_bind_var.get()))
                _core.record(self.tab_view.text21.get("1.0","end-1c"),f)
            else :
                pass
                # os.remove(f)

        except:
            raise Exception("A problem occurred while writing the database.") # Exception or TypeError
        
        finally:
            pass

    def desired_topic_sentences(self):
        self.tab_view.label21.configure(image = self.file_name_to_ctkimage('Blank.png'))
        self.tab_view.label22.configure(text = "Blank Topic")
        self.tab_view.text21.configure(state="normal")
        self.tab_view.text21.delete("1.0", "end")

    def random_topic_image_sentences(self):
        index = random.randint(0, len(self.ImageDataBase)-1)
        LocalDict = self.ImageDataBase[index]
        self.tab_view.label21.configure(image = self.file_name_to_ctkimage(LocalDict["ImageName"]))
        self.tab_view.label22.configure(text = LocalDict["Topic"])
        self.tab_view.text21.configure(state="normal")
        self.tab_view.text21.delete("1.0", "end")
        self.tab_view.text21.insert("0.0", LocalDict["Text"])
        self.tab_view.text21.configure(state="disabled")
        
    def random_topic_text_sentences(self):
        index = random.randint(0, len(self.ImageDataBase)-1)
        LocalDict = self.TopicDataBase[index]
        self.tab_view.label21.configure(image = self.file_name_to_ctkimage(LocalDict["ImageName"]))
        self.tab_view.label22.configure(text = LocalDict["Topic"])
        self.tab_view.text21.configure(state="normal")
        self.tab_view.text21.delete("1.0", "end")
        self.tab_view.text21.insert("0.0", LocalDict["Text"])
        self.tab_view.text21.configure(state="disabled")

    def backward(self):
        if len(self.Words) != 0 :
            index_word = self.tab_view.combo1.get()

            list_words = self.Words
            index_dict = {word: idx for idx, word in enumerate(list_words)}

            selected_index = index_dict[index_word]

            value = len(self.Words)-1 if selected_index-1 == -1 else selected_index-1

            self.tab_view.combo1.set(self.Words[value])

    def forward(self):
        if len(self.Words) != 0 :
            index_word = self.tab_view.combo1.get()

            list_words = self.Words
            index_dict = {word: idx for idx, word in enumerate(list_words)}

            selected_index = index_dict[index_word]

            value = 0 if selected_index+1 == len(self.Words) else selected_index+1

            self.tab_view.combo1.set(self.Words[value])
    
    def import_data_base(self):
        
        try:
            f = askopenfile(initialfile = 'Data.db', defaultextension=".db",filetypes=[("Database","*.db")])
            
            if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            
            file_name, file_extension = os.path.splitext(f.name)
            
            if (file_extension.lower().__eq__(".db")) :
                
                self.Words = self.read_file_in_list(f.name)
                self.tab_view.combo1.configure(values=self.Words)

                try :
                    self.bind_and_update()
                except :
                    self.tab_view.combo1.set("None")

                self.write_list_in_file()    

        except:
            raise Exception("A problem occurred while reading the database.") # Exception or TypeError
        
        finally:
            pass

    def export_data_base(self):
        try:
            f = asksaveasfile(initialfile = 'Data.db', defaultextension=".db",filetypes=[("Database","*.db")])
            
            if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return
            
            file_name, file_extension = os.path.splitext(f.name)

            if (file_extension.lower().__eq__(".db")) :
                with open(f.name, "w") as file:
                    file.writelines(line + "\n" for line in self.Words)
            else :
                f.close()
                os.remove(f.name)

        except:
            raise Exception("A problem occurred while writing the database.") # Exception or TypeError
        
        finally:
            pass

    def change_rate(self,*args):
        # print(self.tab_view.slider1.get())
        pass

    def combobox_callback(self,choice):
        # print("combobox dropdown clicked:", choice)
        pass
    
    def do_nothing(self):
        pass



# if __name__ == "__main__":
#     app = App()
#     app.mainloop()


