import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from datetime import datetime

from dataloader import loadData, plot_Acc, plot_Eda, plot_Temp

def select_folder():
    folder_path = filedialog.askdirectory()
    file_label.config(text=folder_path)
    dates = get_dates_from_folder(folder_path)
    print(dates)
    # TODO: remove all elements from each dropdown and replace them or destroy the menu and recreate one


def get_dates_from_folder(path):
    # get a list of all items in the directory
    items = os.listdir(path)
    folders = []
    for item in items:
        if (os.path.isdir(os.path.join(path, item))):
            date_obj = datetime.strptime(item, '%Y%m%d')
            updated_name = date_obj.strftime('%m/%d/%Y')
            folders.append(updated_name)
    return folders


def set_date_period():
    # get users that are in trials within the slected start and end dates
    users = get_users_within_time_period(start_date.get(), start_date.get())
    print(users)
    # TODO: remove all elements from the user dropdown and replace them or destroy the dropdown and recreate one


def get_users_within_time_period(start_date, end_date):
    users = set()
    path = file_label.cget("text")
    items = os.listdir(path)
    for item in items:
        if (os.path.isdir(os.path.join(path, item))):
            # TODO: make sure the date is within the start date and end date, if so add all of its users (subdirectories to the users set)
            subdirectory_path = os.path.join(path, item)
            subdirectory_items = os.listdir(subdirectory_path)
            for subItem in subdirectory_items:
                if (os.path.isdir(os.path.join(subdirectory_path, subItem))):
                    users.add(subItem)
    return list(users)


def submit():
    filter = {    
        "file_label" : file_label.cget("text"),
        "start_date" : start_date.get(),
        "end_date" : end_date.get(),
        "user" : user.get(),
        "columns": {
            "Acc magnitude avg" : ACC_Mag.get(),
            "Eda avg" : Eda.get(),
            "Temp avg" : temp.get(),
            "Movement intensity" : movement_intensity.get(),
            "Steps count" : step_count.get(),
            "Rest" : rest.get(),
            "On Wrist" : on_wrist.get()
        }
    }
    
    data = loadData(filter)
    
    if "Acc magnitude avg" in data.columns:
        plot_Acc(data)
    
    if "Eda avg" in data.columns:
        plot_Eda(data)
    
    if "Temp avg" in data.columns:
        plot_Temp(data)

    


def create_widgets(root: tk):

    # File selector
    top_label = ttk.Label(root, text="Root Folder")
    top_label.grid(row=0, column=0)

    select_button = ttk.Button(
        root, text="Select folder", command=select_folder)
    select_button.grid(row=1, column=0)

    global file_label
    file_label = ttk.Label(root)
    file_label.grid(row=2, column=0)

    dummy_dates = ['01/18/2020', '01/19/2020', '01/20/2020', '01/21/2020']

    # Start date dropdowns
    start_label = ttk.Label(root, text="Start Date:")
    start_label.grid(row=3, column=0)

    global start_date
    start_date = tk.StringVar()
    global start_date_dropdown
    start_date_dropdown = ttk.OptionMenu(
        root, start_date, dummy_dates[0], *dummy_dates)
    start_date_dropdown.grid(row=4, column=0)

    # End date dropdowns
    end_label = ttk.Label(root, text="End Date:")
    end_label.grid(row=3, column=1)

    global end_date
    end_date = tk.StringVar()
    global end_date_dropdown
    end_date_dropdown = ttk.OptionMenu(
        root, end_date, dummy_dates[0], *dummy_dates)
    end_date_dropdown.grid(row=4, column=1)

    set_dates_button = ttk.Button(
        root, text="Set Dates", command=set_date_period)
    set_dates_button.grid(row=5, column=0)

    # User dropdown
    dummy_users = ['310', '311', '312']

    user_label = tk.Label(root, text="User:")
    user_label.grid(row=6, column=0)

    global user
    user = tk.StringVar()
    global users_dropdown
    users_dropdown = ttk.OptionMenu(
        root, user, dummy_users[0], *dummy_users)
    users_dropdown.grid(row=7, column=0)

    # Graphed Properties
    global ACC_Mag
    ACC_Mag = tk.BooleanVar()
    ACC_Mag_Check = ttk.Checkbutton(
        root, text="ACC Magnitude", variable=ACC_Mag)
    ACC_Mag_Check.grid(row=8, column=0)

    global Eda
    Eda = tk.BooleanVar()
    Eda_Check = ttk.Checkbutton(
        root, text="EDA Average", variable=Eda)
    Eda_Check.grid(row=9, column=0)

    global temp
    temp = tk.BooleanVar()
    Temp_Check = ttk.Checkbutton(
        root, text="Temp Average", variable=temp)
    Temp_Check.grid(row=10, column=0)

    global movement_intensity
    movement_intensity = tk.BooleanVar()
    Move_Check = ttk.Checkbutton(
        root, text="Movement Intensity", variable=movement_intensity)
    Move_Check.grid(row=11, column=0)

    global step_count
    step_count = tk.BooleanVar()
    Step_Check = ttk.Checkbutton(
        root, text="Step Count", variable=step_count)
    Step_Check.grid(row=12, column=0)

    global rest
    rest = tk.BooleanVar()
    Rest_Check = ttk.Checkbutton(
        root, text="Rest", variable=rest)
    Rest_Check.grid(row=13, column=0)

    global on_wrist
    on_wrist = tk.BooleanVar()
    Wrist_Check = ttk.Checkbutton(
        root, text="On Wrist", variable=on_wrist)
    Wrist_Check.grid(row=14, column=0)

    # Submit Button
    submit_button = ttk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=15, column=0)

