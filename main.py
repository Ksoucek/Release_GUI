import json
import os
import tkinter as Tk
from tkinter import ttk
from tkinter import messagebox

#code


def enter_data():
    Instance = Deployment_Instance_entry.get()
    TaskTime = task_time_entry.get()
        
    if Instance and TaskTime:
        PATH_TO_JSON: str = r'C:\NTC\Settings.JSON'
        with open(PATH_TO_JSON, 'r', encoding='utf-8') as f:
         json_content = json.load(f)
         json_content['$DeploymentInstance'] = Instance
         json_content['$TaskTime'] = TaskTime

        with open(PATH_TO_JSON, 'w') as f:
            json.dump(json_content, f, indent=4)

    else:
        tkinter.messagebox.showwarning(title="Error", message="Instance a čas jsou povinné údaje.")
        


window = Tk.Tk()
window.title("Nastavení parametrů releasu")

PATH_TO_JSON: str = r'C:\NTC\Settings.JSON'
with open(PATH_TO_JSON, 'r', encoding='utf-8') as f:
    json_content = json.load(f)
    OldInstance = json_content['$DeploymentInstance'] 
    OldTime =   json_content['$TaskTime'] 
  


frame = Tk.Frame(window)
frame.pack()

text = Tk.StringVar()
text1 = Tk.StringVar()

# Saving User Info
System_Frame =Tk.LabelFrame(frame, text="Release nastavení")
System_Frame.grid(row= 0, column=0, padx=20, pady=10)

Deployment_Instance = Tk.Label(System_Frame, text="Deployment Instance")
Deployment_Instance.grid(row=0, column=0)
TaskTimeLbl = Tk.Label(System_Frame, text="Čas spuštění")
TaskTimeLbl.grid(row=0, column=1)
text1.set(OldInstance)
Deployment_Instance_entry = ttk.Combobox(System_Frame, values=["SSC_ADM", "bc-test","SSC175"],textvariable = text1)



text.set(OldTime)

task_time_entry = Tk.Entry(System_Frame,textvariable = text)
Deployment_Instance_entry.grid(row=1, column=0)
task_time_entry.grid(row=1, column=1)



for widget in System_Frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Accept terms
Email_Frame = Tk.LabelFrame(frame, text="Odeslat emaily k nasazení")
Email_Frame.grid(row=2, column=0, padx=20, pady=15)

SendEmailEntryBefore = Tk.IntVar(value="0")
Sent_before_entry = Tk.Checkbutton(Email_Frame, text= "Odeslat email před nasazením.",
                                  variable=SendEmailEntryBefore, onvalue="1", offvalue="0")
Sent_before_entry.grid(row=0, column=0)

SendEmailEntryAfter= Tk.IntVar(value="0")
Sent_After_entry = Tk.Checkbutton(Email_Frame, text= "Odeslat email po nasazení.",
                                  variable=SendEmailEntryBefore, onvalue="1", offvalue="0")
Sent_After_entry.grid(row=0, column=2)

EmailFromLbl = Tk.Label(Email_Frame, text="Odesilatel Mailu")
Email_From_entry = ttk.Combobox(Email_Frame, values=["jakub.soucek@navitec.cz", "daniel.barnet@navitec.cz"])
EmailFromLbl.grid(row=2, column=0)
Email_From_entry.grid(row=3, column=0)

AplicationPW = Tk.Label(Email_Frame, text="Aplikační heslo Mailu")
AplicationPW_Entry = Tk.Entry(Email_Frame, show="*")
AplicationPW.grid(row=2, column=1)
AplicationPW_Entry.grid(row=3, column=1)


nationality_label = Tk.Label(Email_Frame, text="Odeslat email")
nationality_combobox = ttk.Combobox(Email_Frame, values=["Jen Sobě", "Na seznam příjemců"])
nationality_label.grid(row=2, column=2)
nationality_combobox.grid(row=3, column=2)

# Button
button = Tk.Button(frame, text="Uložit JSON", command= enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)
window.mainloop()