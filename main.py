import json
import subprocess
import ctypes
import tkinter as Tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
import os

# Definice akcí
def run_powershell_script(script_path):
    try:
        command = ["pwsh", "-File", script_path]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return e.stdout, e.stderr

def open_json(path):
    subprocess.call(['notepad.exe', path])

def execute_as_admin(command):
    result = ctypes.windll.shell32.ShellExecuteW(None, "runas", "powershell", command, None, 0)
    if result <= 32:
        raise Exception("Failed to run as admin")

def unschedule_task(command):
    execute_as_admin(command)

def run_task_now(command):
    execute_as_admin(command)

def schedule_task(command):
    execute_as_admin(command)

def load_json(path):
    if not path.exists():
        # Pokud soubor neexistuje, vytvoříme nový s výchozími hodnotami
        default_content = {
            '$TaskName': '',
            '$TaskTime': '',
            '$ReleasedFeatures': '',
            '$EmailFrom': '',
            '$EmailFromPW': '',
            '$EmailTo': '',
            '$Subject': '',
            '$SubjectFinish': '',
            '$Body': '',
            '$BodyFinish': '',
            '$DeploymentInstance': '',
            '$SentEmailBefore': False,
            '$SentEmailAfter': False,
            '$UserID': '',
            '$SendEmailToMyself': False,
            '$DependentAppExist': False
        }
        save_json(path, default_content)
        return default_content
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Pokud je soubor prázdný nebo neplatný JSON, vrátíme prázdný slovník
        return {}

def save_json(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4)

def enter_data():
    instance = Deployment_Instance_entry.get()
    task_time = task_time_entry.get()
    user_id = user_id_entry.get()
    task_name = TaskName_entry.get()
    dependent_app_exist = Newdependent_app_exist.get()

    email_bool_before = NewEmailBoolBefore.get() in ("true", "False")
    email_bool_after = NewEmailBoolAfter.get() in ("true", "False")

    email_from = Email_From_entry.get()
    email_from_pw = AplicationPW_Entry.get()
    email_to = Email_to_Entry.get("1.0", 'end-1c')
    send_email_to_myself = NewSendEmailToMyself.get() in ("true", "False")

    subject = Subject_entry.get()
    body = Body_entry.get("1.0", 'end')
    released_features = ReleasedFeatures_entry.get("1.0", 'end-1c')

    if instance and task_time:
        path_to_json = Path(r'C:\NTC\Settings.JSON')
        json_content = load_json(path_to_json)
        
        json_content.update({
            '$DeploymentInstance': instance,
            '$TaskTime': task_time,
            '$UserID': user_id,
            '$TaskName': task_name,
            '$DependentAppExist': int(dependent_app_exist),
            '$SentEmailBefore': email_bool_before,
            '$SentEmailAfter': email_bool_after,
            '$EmailFrom': email_from,
            '$EmailFromPW': email_from_pw,
            '$EmailTo': email_to,
            '$SendEmailToMyself': send_email_to_myself,
            '$Subject': subject,
            '$Body': body,
            '$ReleasedFeatures': released_features
        })

        save_json(path_to_json, json_content)
    else:
        messagebox.showwarning(title="Error", message="Instance a čas jsou povinné údaje.")

window = Tk.Tk()
window.title("Nastavení parametrů releasu")

# Nastavení ikony okna
# window.iconbitmap(os.path.join(os.path.dirname(__file__), 'path_to_your_icon.ico'))

# Načtení dat do proměnných z JSONu
path_to_json = Path(r'C:\NTC\Settings.JSON')
json_content = load_json(path_to_json)

old_task_name = json_content['$TaskName']
old_task_time = json_content['$TaskTime']
old_released_features = json_content['$ReleasedFeatures']
old_email_from = json_content['$EmailFrom']
old_email_from_pw = json_content['$EmailFromPW']
old_email_to = json_content['$EmailTo']
old_subject = json_content['$Subject']
old_subject_finish = json_content['$SubjectFinish']
old_body = json_content['$Body']
old_body_finish = json_content['$BodyFinish']
old_deployment_instance = json_content['$DeploymentInstance']
old_email_bool_before = json_content['$SentEmailBefore']
old_email_bool_after = json_content['$SentEmailAfter']
old_user_id = json_content['$UserID']
old_send_email_to_myself = json_content['$SendEmailToMyself']
old_dependent_app_exist = json_content['$DependentAppExist']

# Vytvoření okna prostředí
frame = ttk.Frame(window)
frame.pack(padx=20, pady=20, fill="both", expand=True)

# Definice proměnných
old_string1 = Tk.StringVar(value=old_deployment_instance)
old_string2 = Tk.StringVar(value=old_task_time)
old_string3 = Tk.StringVar(value=old_user_id)
old_string4 = Tk.StringVar(value=old_email_from)
old_string5 = Tk.StringVar(value=old_email_from_pw)
old_string6 = Tk.StringVar(value=old_task_name)
old_string7 = Tk.StringVar(value=old_email_to)
old_string8 = Tk.StringVar(value=old_subject)
old_string9 = Tk.StringVar(value=old_body)
old_string10 = Tk.StringVar(value=old_released_features)

# Nastavení releaseu
system_frame = ttk.LabelFrame(frame, text="Release nastavení")
system_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

ttk.Label(system_frame, text="Deployment Instance").grid(row=0, column=0, sticky="w")
Deployment_Instance_entry = ttk.Entry(system_frame, textvariable=old_string1)
Deployment_Instance_entry.grid(row=1, column=0, sticky="ew")

ttk.Label(system_frame, text="Čas spuštění").grid(row=0, column=1, sticky="w")
task_time_entry = ttk.Entry(system_frame, textvariable=old_string2)
task_time_entry.grid(row=1, column=1, sticky="ew")

ttk.Label(system_frame, text="USER ID").grid(row=0, column=2, sticky="w")
user_id_entry = ttk.Entry(system_frame, textvariable=old_string3)
user_id_entry.grid(row=1, column=2, sticky="ew")

ttk.Label(system_frame, text="Název tasku").grid(row=0, column=3, sticky="w")
TaskName_entry = ttk.Entry(system_frame, textvariable=old_string6)
TaskName_entry.grid(row=1, column=3, sticky="ew")

Newdependent_app_exist = Tk.BooleanVar(value=old_dependent_app_exist)
dependent_app_entry = ttk.Checkbutton(system_frame, text="Závislá aplikace", variable=Newdependent_app_exist, onvalue=True, offvalue=False)
dependent_app_entry.grid(row=1, column=4, sticky="w")

for widget in system_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Nastavení Email
email_frame = ttk.LabelFrame(frame, text="Nastavení emailů k releasu")
email_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

NewEmailBoolBefore = Tk.StringVar(value=old_email_bool_before)
ttk.Checkbutton(email_frame, text="Odeslat email před nasazením.", variable=NewEmailBoolBefore, onvalue="true", offvalue="false").grid(row=0, column=0, sticky="w")

NewEmailBoolAfter = Tk.StringVar(value=old_email_bool_after)
ttk.Checkbutton(email_frame, text="Odeslat email po nasazení.", variable=NewEmailBoolAfter, onvalue="true", offvalue="false").grid(row=0, column=1, sticky="w")

ttk.Label(email_frame, text="Odesilatel Mailu").grid(row=1, column=0, sticky="w")
Email_From_entry = ttk.Combobox(email_frame, values=["jakub.soucek@navitec.cz", "daniel.barnet@navitec.cz"], textvariable=old_string4)
Email_From_entry.grid(row=2, column=0, sticky="ew")

ttk.Label(email_frame, text="Aplikační heslo Mailu").grid(row=1, column=1, sticky="w")
AplicationPW_Entry = ttk.Entry(email_frame, show="*", textvariable=old_string5)
AplicationPW_Entry.grid(row=2, column=1, sticky="ew")

NewSendEmailToMyself = Tk.StringVar(value=old_send_email_to_myself)
ttk.Checkbutton(email_frame, text="Odeslat emaily jen sobě", variable=NewSendEmailToMyself, onvalue="true", offvalue="false").grid(row=2, column=2, sticky="w")

ttk.Label(email_frame, text="Seznam příjemců").grid(row=3, column=0, columnspan=3, sticky="w")
Email_to_Entry = scrolledtext.ScrolledText(email_frame, wrap=Tk.WORD, width=80, height=4, font=("Times New Roman", 10))
Email_to_Entry.insert(Tk.INSERT, old_string7.get())
Email_to_Entry.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

ttk.Label(email_frame, text="Předmět mailu").grid(row=5, column=0, columnspan=3, sticky="w")
Subject_entry = ttk.Entry(email_frame, textvariable=old_string8)
Subject_entry.grid(row=6, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

ttk.Label(email_frame, text="Tělo Mailu").grid(row=7, column=0, columnspan=3, sticky="w")
Body_entry = scrolledtext.ScrolledText(email_frame, wrap=Tk.WORD, width=80, height=4, font=("Times New Roman", 10))
Body_entry.insert(Tk.INSERT, old_string9.get())
Body_entry.grid(row=8, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

ttk.Label(email_frame, text="Seznam Požadavků").grid(row=9, column=0, columnspan=3, sticky="w")
ReleasedFeatures_entry = scrolledtext.ScrolledText(email_frame, wrap=Tk.WORD, width=80, height=4, font=("Times New Roman", 10))
ReleasedFeatures_entry.insert(Tk.INSERT, old_string10.get())
ReleasedFeatures_entry.grid(row=10, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

for widget in email_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Tlačítka a akce
button_frame = ttk.Frame(frame)
button_frame.grid(row=2, column=0, pady=20, sticky="ew")

ttk.Button(button_frame, text="Uložit JSON", command=enter_data).grid(row=0, column=0, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Otevři JSON", command=lambda: open_json("C:\\NTC\\Settings.json")).grid(row=0, column=1, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Spustit timer", command=lambda: schedule_task("C:\\NTC\\ScheduledTaskRealease.ps1")).grid(row=0, column=2, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Zrušit timer", command=lambda: unschedule_task("C:\\NTC\\UnscheduleTask.ps1")).grid(row=0, column=3, padx=10, pady=10, sticky="ew")
ttk.Button(button_frame, text="Spustit release hned", command=lambda: run_task_now("C:\\NTC\\ReleaseAndNotificationNow.ps1")).grid(row=0, column=4, padx=10, pady=10, sticky="ew")

for widget in button_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Nastavení dynamického zvětšování a zmenšování
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
system_frame.grid_columnconfigure(0, weight=1)
system_frame.grid_columnconfigure(1, weight=1)
system_frame.grid_columnconfigure(2, weight=1)
system_frame.grid_columnconfigure(3, weight=1)
system_frame.grid_columnconfigure(4, weight=1)
email_frame.grid_columnconfigure(0, weight=1)
email_frame.grid_columnconfigure(1, weight=1)
email_frame.grid_columnconfigure(2, weight=1)
email_frame.grid_columnconfigure(3, weight=1)
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)
button_frame.grid_columnconfigure(3, weight=1)
button_frame.grid_columnconfigure(4, weight=1)

window.mainloop()