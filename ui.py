import os
from typing import List
import tkinter as tk
from tkinter import *

from tkinter import ttk, Button

from datetime import datetime
from Plot import DataPlot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from dataloader import loadData, createDataPlotObjects, plot_ChangeTime, Graph

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
        errorMessage = "Start Date cannot be greater than the End Date."
    return errorMessage


def set_users_in_date_period(root):
    previousUser = user.get()
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
        if previousUser in users:
            user.set(previousUser)
        else:
            user.set(users[0])
    else:
        # reset selected user
        user.set("")
        # empty users dropdown
        users_dropdown['menu'].delete(0, 'end')
        # show error message popup
        showErrorPopup(root, errorMessage)


def get_users_within_time_period(start_date: str, end_date: str):
    start = datetime.strptime(
        start_date, "%m/%d/%Y").strftime('%Y%m%d')
    end = datetime.strptime(end_date, "%m/%d/%Y").strftime('%Y%m%d')
    users = set()
    for date_folder in os.listdir(datasetPath):
        if start <= date_folder <= end:
            for user_folder in os.listdir(os.path.join(datasetPath, date_folder)):
                if os.path.isdir(os.path.join(datasetPath, date_folder, user_folder)):
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
        errorMessage = "Start Date cannot be greater than the End Date."
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
        data = loadData(filter, datasetPath)
        # create a DataPlot class object for each column property within the pandas dataframe
        global dataPlots
        dataPlots = createDataPlotObjects(data)
        # plot all selected properties simultaneously
        plot_selected_properties(dataPlots, root)

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

    # Create a style object
    style = ttk.Style()

    # Set the style's background color to match the root
    style.configure(".", background=root.cget("background"))

    dates = get_dates_from_folder()

    # Title label
    title_label = ttk.Label(
        root, text="Wearable Sensor Data Application", font=("Arial", 20))
    title_label.grid(row=0, column=0, columnspan=5)

    # Start date dropdowns
    start_label = ttk.Label(root, text="Start Date:")
    start_label.grid(row=3, column=0, pady=5)

    global start_date
    start_date = tk.StringVar()
    global start_date_dropdown
    start_date_dropdown = ttk.OptionMenu(
        root, start_date, dates[0], *dates, command=lambda _: set_users_in_date_period(root))
    start_date_dropdown.grid(row=4, column=0)

    # End date dropdowns
    end_label = ttk.Label(root, text="End Date:")
    end_label.grid(row=3, column=1, pady=5)

    global end_date
    end_date = tk.StringVar()
    global end_date_dropdown
    end_date_dropdown = ttk.OptionMenu(
        root, end_date, dates[0], *dates, command=lambda _: set_users_in_date_period(root))
    end_date_dropdown.grid(row=4, column=1)

    # User dropdown
    user_label = ttk.Label(root, text="User:")
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

    user_label = ttk.Label(root, text="Select Properties:")
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

   

    variable = StringVar(root)

    w = OptionMenu(root, variable ,"Line", "Scatter", "Bar")
    w.grid(row=12, column=1)


def plot_selected_properties(dataPlots, root):
    # create popup window for plots
    new_window = tk.Toplevel(root)
    new_window.geometry('1000x800')

    colors = ['red', 'green', 'blue', 'maroon', 'purple', 'pink', 'orange']

    i = 0
    for dataPlot in dataPlots:
        # create a Matplotlib figure and axis
        # create a figure with a size of 5x4 inches and a DPI of 100
        fig = Figure(figsize=(2, 1), dpi=100)
        ax = fig.add_subplot(111)  # create a single subplot within the figure

        # plot some data on the subplot
        line, = ax.plot(dataPlot.times, dataPlot.values,
                        label=dataPlot.propertyName, color=colors[i])

        ax.xaxis.set_major_locator(MaxNLocator(20))
        # slant the x-axis tick labels
        ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha='center')
        ax.legend(handles=[line], loc='upper left')  # add a legend to the plot

        # adjust subplot spacing
        fig.subplots_adjust(bottom=0.3, top=0.7)

        # create a canvas to display the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=new_window)

        # draw the figure on the canvas
        canvas.draw()

        # add the canvas to the Tkinter window using grid()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
        i += 1
        
#Sliders
    current_left_value = tk.IntVar()
    current_right_value = tk.IntVar()
    def get_current_left_value():
       return '{: .2f}'.format(current_left_value.get())
    
    def get_current_right_value():
        return '{: .2f}'.format(current_right_value.get())
    def left_slider_changed(event):
        value_left_label.configure(text=get_current_left_value())
    def right_slider_changed(event):
        value_right_label.configure(text=get_current_right_value())
       
    
    slider_right = ttk.Scale(new_window,from_=0,to=1500,orient='horizontal',command=right_slider_changed,variable=current_right_value)
    slider_right.pack(side = 'right',fill ='both', expand = True)
    slider_right_label = ttk.Label(new_window,text='Right time filter:')
    slider_right_label.pack(side = 'right',fill ='both', expand = True)
    slider_left = ttk.Scale(new_window,from_=0,to=1500,orient='horizontal',command=left_slider_changed,variable=current_left_value)
    slider_left.pack(side = 'right',fill ='both', expand = True)
    slider_left_label = ttk.Label(new_window,text='Left time filter:')
    slider_left_label.pack(side = 'right',fill ='both', expand = True)
    value_right_label = ttk.Label(new_window,text=get_current_right_value())
    value_right_label.pack(side =  'right',fill = 'both', expand = True)
    value_left_label = ttk.Label(new_window,text=get_current_left_value())
    value_left_label.pack(side =  'right',fill = 'both', expand = True)
    variable = StringVar(new_window)
    w = OptionMenu(new_window, variable ,"Line", "Scatter", "Bar")
    w.pack(side =  'right',fill = 'both', expand = True)
    def callback():
        fll = float(get_current_left_value())
        flr = float(get_current_right_value())
        #plotProperties(dataPlots, fl)
        
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

    # Create panda's dataframe using the filtered data and change the time using plt.xlim.
        data = loadData(filter)
        graphType = variable.get()
        print(graphType)
        plot_ChangeTime(data,fll,flr)
        dataPlots = createDataPlotObjects(data)

    # plot each of the data plots
       #plotProperties(dataPlots)
        plot_selected_properties_lim(dataPlots, root, fll, flr, graphType)
        #print(get_current_value())
        #dataPlot[times].length

    b = Button(new_window, text = "Change Scope", width = 10, command = callback)
    b.pack(side = 'bottom',fill = 'both', expand = False)
    

def plot_selected_properties_lim(dataPlots, root, leftLim, rightLim, graphType):
    # create popup window for plots
    new_window = tk.Toplevel(root)
    new_window.geometry('1000x1000')

    colors = ['red', 'green', 'blue', 'maroon', 'purple', 'pink', 'orange']
     
    i = 0
    for dataPlot in dataPlots:
        # create a Matplotlib figure and axis
        
        fig = Figure(figsize=(2, 1), dpi=100)  # create a figure with a size of 5x4 inches and a DPI of 100
        ax = fig.add_subplot(111)  # create a single subplot within the figure
        #ax.xaxis.set_major_locator(MaxNLocator(20))
        # slant the x-axis tick labels
        #ax.set_xticklabels(ax.get_xticklabels(), rotation=15, ha='center')
        ax.set_xlim(left = leftLim, right = rightLim)
        # plot some data on the subplot
        if(graphType == "Bar"):
            line, = ax.bar(dataPlot.times, dataPlot.values, label=dataPlot.propertyName, color=colors[i])
        elif (graphType == "Scatter"):
            line, = ax.scatter(dataPlot.times, dataPlot.values, label=dataPlot.propertyName, color=colors[i])
        else:
            line, = ax.plot(dataPlot.times, dataPlot.values, label=dataPlot.propertyName, color=colors[i])
        #plt.xlim(line, left = leftLim, right = rightLim)
        ax.legend(handles=[line], loc='upper left')  # add a legend to the plot
        
        # create a canvas to display the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=new_window)

        # draw the figure on the canvas
        canvas.draw()

        # add the canvas to the Tkinter window using grid()
        canvas.get_tk_widget().pack(side='top', fill='both', expand=True)
        i += 1

    #Sliders
    current_left_value = tk.IntVar()
    current_right_value = tk.IntVar()
    def get_current_left_value():
       return '{: .2f}'.format(current_left_value.get())
    
    def get_current_right_value():
        return '{: .2f}'.format(current_right_value.get())
    def left_slider_changed(event):
        value_left_label.configure(text=get_current_left_value())
    def right_slider_changed(event):
        value_right_label.configure(text=get_current_right_value())
       
    
    slider_right = ttk.Scale(new_window,from_=0,to=1500,orient='horizontal',command=right_slider_changed,variable=current_right_value)
    slider_right.pack(side = 'right',fill ='both', expand = True)
    slider_right_label = ttk.Label(new_window,text='Right time filter:')
    slider_right_label.pack(side = 'right',fill ='both', expand = True)
    slider_left = ttk.Scale(new_window,from_=0,to=1500,orient='horizontal',command=left_slider_changed,variable=current_left_value)
    slider_left.pack(side = 'right',fill ='both', expand = True)
    slider_left_label = ttk.Label(new_window,text='Left time filter:')
    slider_left_label.pack(side = 'right',fill ='both', expand = True)
    value_right_label = ttk.Label(new_window,text=get_current_right_value())
    value_right_label.pack(side =  'right',fill = 'both', expand = True)
    value_left_label = ttk.Label(new_window,text=get_current_left_value())
    value_left_label.pack(side =  'right',fill = 'both', expand = True)
    def callback():
        fll = float(get_current_left_value())
        flr = float(get_current_right_value())
        #plotProperties(dataPlots, fl)
        
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

    # Create panda's dataframe using the filtered data and change the time using plt.xlim.
        data = loadData(filter)
        plot_ChangeTime(data,fll,flr)
        dataPlots = createDataPlotObjects(data)

    # plot each of the data plots
       #plotProperties(dataPlots)
        plot_selected_properties_lim(dataPlots, root,fll,flr)
        #print(get_current_value())
        #dataPlot[times].length

    b = Button(new_window, text = "Change Scope", width = 10, command = callback)
    b.pack(side = 'bottom',fill = 'both', expand = False)


