from ui import *

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x500")
    root.configure(bg="#CCE5F0')
    # Center elements vertically
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(13, weight=1)
    
    # Center elements horizontally
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.title("Wearable Sensor Data Application")

    create_widgets(root)

    root.mainloop()
