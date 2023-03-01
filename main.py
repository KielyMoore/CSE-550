import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import datetime


def select_folder():
    folder_path = filedialog.askdirectory()
    file_path.set(folder_path)


def get_users_for_trials():
    print("this will be used to get all of the users that have trials between the start and stop date")


def submit():
    print('submit the loader data to the backend')


def create_widgets():

    # File selector
    top_label = ttk.Label(root, text="Base Folder")
    top_label.grid(row=0, column=0)

    select_button = ttk.Button(
        root, text="Select folder", command=select_folder)
    select_button.grid(row=1, column=0)

    file_label = ttk.Label(root, textvariable=file_path)
    file_label.grid(row=2, column=0)

    # start and end date selector
    current_date = datetime.date.today()
    years = list(range(2000, 2023))
    months = list(range(1, 13))
    days = list(range(1, 32))

    # Start date dropdowns
    start_label = ttk.Label(root, text="Start Date:")
    start_label.grid(row=3, column=0)

    month_var = tk.StringVar()
    month_dropdown = ttk.OptionMenu(
        root, month_var, current_date.month, *months)
    month_dropdown.grid(row=4, column=0)

    day_var = tk.StringVar()
    day_dropdown = ttk.OptionMenu(root, day_var, current_date.day, *days)
    day_dropdown.grid(row=4, column=1)

    year_var = tk.StringVar()
    year_dropdown = ttk.OptionMenu(root, year_var, current_date.year, *years)
    year_dropdown.grid(row=4, column=2)

    # End date dropdowns
    end_label = ttk.Label(root, text="End Date:")
    end_label.grid(row=3, column=3)

    end_month_var = tk.StringVar()
    end_month_dropdown = ttk.OptionMenu(
        root, end_month_var, current_date.month, *months)
    end_month_dropdown.grid(row=4, column=3)

    end_day_var = tk.StringVar()
    end_day_dropdown = ttk.OptionMenu(
        root, end_day_var, current_date.day, *days)
    end_day_dropdown.grid(row=4, column=4)

    end_year_var = tk.StringVar()
    end_year_dropdown = ttk.OptionMenu(
        root, end_year_var, current_date.year, *years)
    end_year_dropdown.grid(row=4, column=5)

    # User textbox
    user_label = tk.Label(root, text="User:")
    user_label.grid(row=5, column=0)

    users = [310, 311, 312]
    user = tk.StringVar()
    end_year_dropdown = ttk.OptionMenu(
        root, user, users[0], *users)
    end_year_dropdown.grid(row=6, column=0)

    # Graphed Properties
    ACC_Mag = tk.BooleanVar()
    ACC_Mag_Check = ttk.Checkbutton(
        root, text="ACC Magnitude", variable=ACC_Mag)
    ACC_Mag_Check.grid(row=7, column=0)

    Eda = tk.BooleanVar()
    Eda_Check = ttk.Checkbutton(
        root, text="EDA Average", variable=Eda)
    Eda_Check.grid(row=8, column=0)

    temp = tk.BooleanVar()
    Temp_Check = ttk.Checkbutton(
        root, text="Temp Average", variable=temp)
    Temp_Check.grid(row=9, column=0)

    submit_button = ttk.Button(root, text="Submit", command=submit)
    submit_button.grid(row=10, column=0)


root = tk.Tk()
root.geometry("1080x720")
root.title("Folder Selector")

file_path = tk.StringVar()

create_widgets()

root.mainloop()
