import os
from typing import List
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from Plot import DataPlot
from dataloader import loadData, createDataPlotObjects, plot_Acc, plot_Eda, plot_Temp, pd, plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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


def set_date_period():
    # get users that are in trials within the selected start and end dates
    # users = get_users_within_time_period(start_date.get(), start_date.get())
    print("set user's dropdown values based off of selected dates")
    # TODO: remove all elements from the user dropdown and replace them or destroy the dropdown and recreate one


def get_users_within_time_period(start_date: str, end_date: str):
    users = set()
    items = os.listdir(datasetPath)
    for item in items:
        if (os.path.isdir(os.path.join(datasetPath, item))):
            # TODO: make sure the date is within the start date and end date, if so add all of its users (subdirectories to the users set)
            subdirectory_path = os.path.join(datasetPath, item)
            subdirectory_items = os.listdir(subdirectory_path)
            for subItem in subdirectory_items:
                if (os.path.isdir(os.path.join(subdirectory_path, subItem))):
                    users.add(subItem)
    return list(users)


def submit(root: tk):
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

    # plot all selected properties simultaneously
    plot_selected_properties(dataPlots, root)

def create_widgets(root: tk):

    dummy_dates = get_dates_from_folder()
    # ['01/18/2020', '01/19/2020', '01/20/2020', '01/21/2020']

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

    global localTime
    localTime = tk.BooleanVar(value=True)
    Local_Time_Check = ttk.Checkbutton(
        root, text="Local Time", variable=localTime)
    Local_Time_Check.grid(row=8, column=0)

    # Graphed Properties

    user_label = tk.Label(root, text="Select Properties:")
    user_label.grid(row=9, column=0)

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
    submit_button = ttk.Button(root, text="Submit", command=lambda: submit(root))
    submit_button.grid(row=12, column=0)

def plot_selected_properties(dataPlots, root):
    # create popup window for plots
    new_window = tk.Toplevel(root)
    new_window.geometry('1000x1000')

    colors = ['red', 'green', 'blue', 'maroon', 'purple', 'pink', 'orange']

    i = 0
    for dataPlot in dataPlots:
        # create a Matplotlib figure and axis
        fig = Figure(figsize=(2, 1), dpi=100)  # create a figure with a size of 5x4 inches and a DPI of 100
        ax = fig.add_subplot(111)  # create a single subplot within the figure

        # plot some data on the subplot
        line, = ax.plot(dataPlot.times, dataPlot.values, label=dataPlot.propertyName, color=colors[i])
        ax.legend(handles=[line], loc='upper left')  # add a legend to the plot

        # create a canvas to display the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=new_window)

        # draw the figure on the canvas
        canvas.draw()

        # add the canvas to the Tkinter window using grid()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
        i += 1


