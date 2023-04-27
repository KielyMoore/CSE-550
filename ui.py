import os
from typing import List
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from Plot import DataPlot

from dataloader import loadData, createDataPlotObjects, plot_Acc, plot_Eda, plot_Temp

datasetPath = "./Dataset/"

# get dates for the dates dropdown on the dataloader


def get_dates_from_folder():
    # get a list of all items in the directory
    items = os.listdir(datasetPath)
    dates = []
    for item in items:
        if (os.path.isdir(os.path.join(datasetPath, item))):
            date_obj = datetime.strptime(item, '%Y%m%d')
            updated_name = date_obj.strftime('%m/%d/%Y')
            dates.append(updated_name)
    return dates


# plot the data properties
def plotProperties(dataPlots: List[DataPlot]):
    for dataPlot in dataPlots:
        dataPlot.get_plot().show()


def validateDates():
    errorMessage = ""
    if start_date.get() > end_date.get():
        errorMessage = "End Date cannot be greater than the Start Date."
    return errorMessage


def set_users_in_date_period(root):
    # reset selected user
    user.set("")
    # generate an error message if needed
    errorMessage = validateDates()
    if errorMessage == "":
        # get users that are in trials within the selected start and end dates
        users = get_users_within_time_period(start_date.get(), end_date.get())
        # Update the dropdown menu with the list of users
        users_dropdown['menu'].delete(0, 'end')
        for userString in users:
            users_dropdown['menu'].add_command(
                label=userString, command=tk._setit(user, userString))
        user.set(users[0])
    else:
        # empty users dropdown
        users_dropdown['menu'].delete(0, 'end')
        # show error message popup
        showErrorPopup(root, errorMessage)


def get_users_within_time_period(start_date: str, end_date: str):
    start = datetime.strptime(
        start_date, "%m/%d/%Y").strftime('%Y%m%d')
    end = datetime.strptime(end_date, "%m/%d/%Y").strftime('%Y%m%d')
    users = set()
    for date_folder in os.listdir("./Dataset"):
        if start <= date_folder <= end:
            for user_folder in os.listdir(os.path.join("Dataset", date_folder)):
                if os.path.isdir(os.path.join("Dataset", date_folder, user_folder)):
                    users.add(user_folder)
    return sorted(list(users))


def validateUserWithinDateRange():
    usersWithinSpecifiedDates = get_users_within_time_period(
        start_date.get(), end_date.get())
    if user.get() in usersWithinSpecifiedDates:
        return True
    else:
        return False


def validateForm():
    errorMessage = ""
    if start_date.get() > end_date.get():
        errorMessage = "End Date cannot be greater than the Start Date."
    elif user.get() == "":
        errorMessage = "Please select a User to load data for."
    elif not ACC_Mag.get() and not Eda.get() and not temp.get() and not movement_intensity.get() and not step_count.get() and not rest.get() and not on_wrist.get():
        errorMessage = "Please select atleast one data property to view."
    elif not validateUserWithinDateRange():
        errorMessage = "Selected user doesn't have recorded data within the specified date range."
    return errorMessage


def submit(root):
    errorMessage = validateForm()
    if errorMessage == "":
        filter = {
            "start_date": start_date.get(),
            "end_date": end_date.get(),
            "user": user.get(),
            "localTime": localTime.get(),
            "columns": {
                "Acc magnitude avg": ACC_Mag.get(),
                "Eda avg": Eda.get(),
                "Temp avg": temp.get(),
                "Movement intensity": movement_intensity.get(),
                "Steps count": step_count.get(),
                "Rest": rest.get(),
                "On Wrist": on_wrist.get()
            }
        }
        print(filter)
        # create panda's dataframe
        data = loadData(filter)
        # create a DataPlot class object for each column property within the pandas dataframe
        global dataPlots
        dataPlots = createDataPlotObjects(data)
        # plot each of the data plots
        plotProperties(dataPlots)

    else:
        showErrorPopup(root, errorMessage)


def showErrorPopup(root, message):
    # Disable the main window while the error popup is displayed
    root.attributes('-disabled', True)
    # Create the error popup
    error_popup = tk.Toplevel(root)
    error_popup.title('Error')
    error_popup.geometry('350x200')
    # Set the popup to be on top of other windows
    error_popup.attributes('-topmost', True)
    # Set the function to call when the user closes the popup
    error_popup.protocol("WM_DELETE_WINDOW",
                         lambda: close_popup(root, error_popup))
    # Create the message label
    message_label = ttk.Label(error_popup, text=message, font=(
        'Arial', 14), wraplength=250, justify='center')
    message_label.pack(pady=20)
    # Create the exit button
    exit_button = ttk.Button(error_popup, text='Exit', style='Exit.TButton',
                             command=lambda: close_popup(root, error_popup))
    exit_button.pack(pady=10)
    # Center the error popup on the root window
    error_popup.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - error_popup.winfo_reqwidth()) / 2
    y = root.winfo_y() + (root.winfo_height() - error_popup.winfo_reqheight()) / 2
    error_popup.geometry("+%d+%d" % (x, y))
    # Wait for the error popup to be closed
    error_popup.wait_window()


def close_popup(root, popup):
    # Enable the main window and destroy the popup
    root.attributes('-disabled', False)
    popup.destroy()


def create_widgets(root: tk):

    dates = get_dates_from_folder()

    # Title label
    title_label = ttk.Label(
        root, text="Wearable Sensor Data Application", font=("TkDefaultFont", 20))
    title_label.grid(row=0, column=0, columnspan=5)

    # Start date dropdowns
    start_label = ttk.Label(root, text="Start Date:")
    start_label.grid(row=3, column=0, pady=5)

    global start_date
    start_date = tk.StringVar()
    global start_date_dropdown
    start_date_dropdown = ttk.OptionMenu(
        root, start_date, dates[0], *dates)
    start_date_dropdown.grid(row=4, column=0)

    # End date dropdowns
    end_label = ttk.Label(root, text="End Date:")
    end_label.grid(row=3, column=1, pady=5)

    global end_date
    end_date = tk.StringVar()
    global end_date_dropdown
    end_date_dropdown = ttk.OptionMenu(
        root, end_date, dates[0], *dates)
    end_date_dropdown.grid(row=4, column=1)

    set_dates_button = ttk.Button(
        root, text="Set Dates", command=lambda: set_users_in_date_period(root))
    set_dates_button.grid(row=4, column=2)

    # User dropdown
    user_label = tk.Label(root, text="User:")
    user_label.grid(row=6, column=0, pady=20)

    global user
    user = tk.StringVar()
    global users_dropdown
    users_dropdown = ttk.OptionMenu(
        root, user, '')
    users_dropdown.grid(row=6, column=1)

    global localTime
    localTime = tk.BooleanVar(value=True)
    Local_Time_Check = ttk.Checkbutton(
        root, text="Local Time", variable=localTime)
    Local_Time_Check.grid(row=8, column=0, pady=5)

    # Graphed Properties

    user_label = tk.Label(root, text="Select Properties:")
    user_label.grid(row=9, column=0, pady=5)

    global ACC_Mag
    ACC_Mag = tk.BooleanVar()
    ACC_Mag_Check = ttk.Checkbutton(
        root, text="ACC Magnitude", variable=ACC_Mag)
    ACC_Mag_Check.grid(row=10, column=0)

    global Eda
    Eda = tk.BooleanVar()
    Eda_Check = ttk.Checkbutton(
        root, text="EDA Average", variable=Eda)
    Eda_Check.grid(row=10, column=1)

    global temp
    temp = tk.BooleanVar()
    Temp_Check = ttk.Checkbutton(
        root, text="Temp Average", variable=temp)
    Temp_Check.grid(row=10, column=2)

    global movement_intensity
    movement_intensity = tk.BooleanVar()
    Move_Check = ttk.Checkbutton(
        root, text="Movement Intensity", variable=movement_intensity)
    Move_Check.grid(row=10, column=3)

    global step_count
    step_count = tk.BooleanVar()
    Step_Check = ttk.Checkbutton(
        root, text="Step Count", variable=step_count)
    Step_Check.grid(row=11, column=0)

    global rest
    rest = tk.BooleanVar()
    Rest_Check = ttk.Checkbutton(
        root, text="Rest", variable=rest)
    Rest_Check.grid(row=11, column=1)

    global on_wrist
    on_wrist = tk.BooleanVar()
    Wrist_Check = ttk.Checkbutton(
        root, text="On Wrist", variable=on_wrist)
    Wrist_Check.grid(row=11, column=2)

    # Submit Button
    submit_button = ttk.Button(
        root, text="Submit", command=lambda: submit(root))
    submit_button.grid(row=12, column=0, pady=15, padx=10)
