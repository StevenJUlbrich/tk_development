import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Tkinter Tabs Example")

# Create the notebook widget
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Create two frames for two tabs
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)

# Add frames as tabs to the notebook
notebook.add(tab1, text='Tab 1')
notebook.add(tab2, text='Tab 2')

# Add content to the first tab
label1 = ttk.Label(tab1, text="This is the content of the first tab")
label1.pack(padx=10, pady=10)

# Add content to the second tab
label2 = ttk.Label(tab2, text="This is the content of the second tab")
label2.pack(padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
