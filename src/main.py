from calendar import c
import email
from email.mime import image
from math import e
from operator import ge
from tkinter import N, image_names, ttk, Menu
import tkinter as tk
import os
from tkinter import messagebox as tmsg
from tkinter import Tk, Frame, Label, Entry, Button, StringVar, OptionMenu
from wsgiref import validate
from PIL import Image, ImageTk
import re
from datetime import date, datetime
from tkinter import filedialog
import sqlite3
import comm
from numpy import delete, save
from ttkwidgets.autocomplete import AutocompleteEntry

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' # Email Validation


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        x, y, _, _ = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + self.widget.winfo_rooty() + 25

        # Create a toplevel window and position it.
        self.tooltip = Tk()
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        # label to display the tooltip text.
        label = ttk.Label(
            self.tooltip,
            text=self.text,
            background="#FFFFDD",
            relief="solid",
            borderwidth=1,
            font=("TkDefaultFont", 10, "bold"),
        )
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class PlaceholderMixin:
    def remove_placeholder(self, event):
        """Remove placeholder text, if present"""
        placeholder_text = getattr(event.widget, "placeholder_text", "")
        if placeholder_text and event.widget.get() == placeholder_text:
            event.widget.delete(0, "end")
            event.widget.config(fg="black")
        elif placeholder_text and event.widget.get() != placeholder_text:
            event.widget.config(fg="black")

    def add_placeholder(self, event):
        """ " add placeholder text, if needed"""
        placeholder_text = getattr(event.widget, "placeholder", "")
        if placeholder_text and event.widget.get() == "":
            event.widget.insert(0, placeholder_text)
            event.widget.config(fg="white")
        elif placeholder_text and event.widget.get() != "":
            event.widget.config(fg="white")

    def init_placeholder(self, widget, placeholder_text):
        """initialize placeholder text"""
        widget.placeholder_text = placeholder_text
        if widget.get() == "":
            widget.insert("end", placeholder_text)
            # Setup bindings to remove/add placeholder text
            widget.bind("<FocusIn>", self.remove_placeholder)
            widget.bind("<FocusOut>", self.add_placeholder)


class Date_Validation:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.widget.bind("<Return>", self.ins_value)

    def ins_value(self, event):
        if self.widget.get() == "":
            self.widget.delete(0, "end")
            self.widget.insert( 0, self.text)
            self.widget.tx_focusNext().focus()
        else:
            self.widget.tk_focusNext().focus()

class CreateImageToolTip:

    def __init__(self, widget, treeview, text = 'tooltip'):
        self.widget = widget
        self.treeview = treeview
        self.text = text
        self.tooltip = None
        self.id = None
        self.x = self.y = 0

    def show_tooltip(self, item, event=None):
        if item and item in self.treeview.selection():
            item_values = self.treeview.item(item, "values")
            if item_values and len(item_values) >= 2:
                image_path = f"./resource/image/{item_values[0]}.jpg"
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    image.thumbnail((130, 140))
                    photo = ImageTk.PhotoImage(image)

                    # Ensure the self.x and self.y are set to the current mouse position
                    if event:
                        self.x = event.x_root
                        self.y = event.y_root

                    self.tooltip = tk.Toplevel(self.widget)
                    self.tooltip.wm_overrideredirect(True)
                    self.tooltip.wm_geometry(f"+{self.x + 15}+{self.y + 10}")
                    
                    label = Label(self.tooltip, image=photo, text=self.text, justify='left', background="#FFFFDD", relief="solid", borderwidth=1)
                    #label.pack(ipadx=1)

                    #label = Label(self.tooltip, image=photo, relief="solid", borderwidth=1)
                    label.image = photo
                    label.pack(ipadx=1)
                    
                    self.id = photo

                else:
                    self.hide_tooltip()

    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
            self.id = None
            self.x = self.y = 0





        
class Myapp(PlaceholderMixin):
    def __init__(self, window):
        super().__init__()
        self.window = window
        window.title("Student Info")
        f_w = 1280
        f_h = 830
        window.iconbitmap(window, r"./resource/microsoft.ico")
        window.config(bg="#B0D9B1")
        screen_w = window.winfo_screenwidth()
        screen_h = window.winfo_screenheight()
        x = (screen_w / 2) - (f_w / 2)
        y = (screen_h / 2) - (f_h / 2)
        window.geometry("%dx%d+%d+%d" % (f_w, f_h, x, y))
        # -----------------------------------------------
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.map("TCombobox", fieldbackground=[("focus", "#FFFB73")])
        self.style.configure(
            "TreeView.Heading",
            font=("Courier New", 13, "bold"),
            background="#B0D9B1",
            foreground="#186F65",
        )
        self.style.configure(
            "Treeview",
            font=("Courier New", 12, "bold"),
            background="#B0D9B1",
            foreground="#186F65",
        )
        self.style.map("TEntry", fieldbackground=[("focus", "#FFFB73")])
        self.style.configure("TEntry", borderwwidth =[("focus", 0)])
        # -----------------------------------------------
        self.frame_head = Frame(
            self.window,
            highlightbackground="#739072",
            highlightthickness=2,
            bg="#739072",
            relief="raised",
            height=60,
        )
        self.frame_head.pack(side="top", anchor="n", fill="x")
        # -----------------------------------------------

        self.frame_grid = Frame(
            self.window,
            highlightbackground="#739072",
            highlightthickness=2,
            bg="#739072",
            relief="raised",
            height=350,
        )

        self.frame_grid.pack(side="bottom", anchor="s", fill="x")
        # -----------------------------------------------

        self.frm_ctrl = Frame(
            self.window,
            highlightbackground="#557C55",
            highlightthickness=2,
            bg="#B0D9B1",
        )
        self.frm_ctrl.pack(padx=20, pady=20, side="left", anchor="nw")
        # -----------------------------------------------
        self.frm_8 = Frame(
            self.window,
            highlightbackground="#557C55",
            highlightthickness=2,
            bg="#6AA984",
        )
        self.frm_8.pack(padx=0, pady=0, side="right", anchor="ne", fill="y")

        self.frm_btn = Frame(
            self.frm_8,
            highlightbackground="#557C55",
            highlightthickness=2,
            bg="#6AA984",
        )
        self.frm_btn.pack(padx=0, pady=100, side="top", anchor="ne", fill="y")

        # -----------------------------------------------
        self.frm_11 = Frame(self.window, bg="#B0D9B1", height=30)
        self.frm_11.pack(side="right", anchor="s", fill="x")

        # +++++++++++++++++++++++++++++++++++++++++++++++

        self.frm_2 = Frame(self.frm_ctrl, bg="#B0D9B1")
        self.frm_2.grid(column=1, row=2, sticky="ew", padx=0, pady=0)
        # -----------------------------------------------
        self.frm_3 = Frame(self.frm_ctrl, bg="#B0D9B1")
        self.frm_3.grid(column=1, row=3, sticky="ew", padx=0, pady=0)
        # -----------------------------------------------
        self.frm_4 = Frame(self.frm_ctrl, bg="#B0D9B1")
        self.frm_4.grid(column=1, row=4, sticky="ew", padx=0, pady=0)
        # -----------------------------------------------
        self.frm_5 = Frame(self.frm_ctrl, bg="#B0D9B1")
        self.frm_5.grid(column=1, row=5, sticky="ew", padx=0, pady=0)
        # -----------------------------------------------
        self.frm_6 = Frame(self.frm_ctrl, bg="#B0D9B1")
        self.frm_6.grid(column=1, row=6, sticky="ew", padx=0, pady=0)
        # -----------------------------------------------
        self.frm_10 = Frame(self.frm_ctrl, bg="#B0D9B1")
        self.frm_10.grid(column=1, row=6, sticky="e", padx=0, pady=0)

        # -----------------------------------------------
        self.frm_7 = Frame(self.frm_ctrl, bg="#B0D9B1")
        self.frm_7.grid(column=2, row=1, rowspan=7, sticky="n", padx=0, pady=0)

        # -----------------------------------------------
        self.frm_12 = Frame(self.frm_11, bg="#B0D9B1")
        self.frm_12.pack(side="right", anchor="e", fill="y")

        # -----------------------------------------------
        self.frm_1 = Frame(self.frm_ctrl, bg="#B0D9B1")
        self.frm_1.grid(column=1, row=1, sticky="ew", padx=0, pady=0)
        self.image_folder_path = "./resource/image/"
        self.data = None
        self.name = [] #Added for Autocomplete change from None to empty list guarantees that self.name can be safely passed to AutocompleteEntry even if the subsequent data loading fails or if self.name is not updated for some reason
        self.load_autocomplete() # Added for Autocomplete




        self.frm_control()

        # Validate Input -------------------------------
        self.txt_contact_number.configure(
            validate="key",
            validatecommand=(
                self.txt_contact_number.register(self.validate_input),
                "%P",
                1000000000000,
            ),
        )
        self.txt_day.configure(
            validate="key",
            validatecommand=(self.txt_day.register(self.validate_input), "%P", 100),
        )
        self.txt_month.configure(
            validate="key",
            validatecommand=(self.txt_month.register(self.validate_input), "%P", 100),
        )
        self.txt_year.configure(
            validate="key",
            validatecommand=(self.txt_year.register(self.validate_input), "%P", 10000),
        )

        # Menu Strip -----------------------------------
        self.content_menu = Menu(self.window, tearoff=0)
        self.content_menu.add_command(label ='Edit', command = self.edit_item)
        self.content_menu.add_command(label ='Delete', command = self.delete_item)



        # Date Validation ------------------------------
        Date_Validation(self.txt_day, datetime.now().strftime("%d/$m/%Y")[0:2])
        Date_Validation(self.txt_month, datetime.now().strftime("%d/$m/%Y")[3:5])
        Date_Validation(self.txt_year, datetime.now().strftime("%d/$m/%Y")[6:])

        # Bind Tool Tip to Buttons ----------------------
        Tooltip(self.btn_save, "Ctrl+S")
        window.bind("<Control-s>", lambda event: self.btn_save.invoke())
        
        Tooltip(self.btn_update, "Ctrl+U")
        window.bind("<Control-u>", lambda event: self.btn_update.invoke())

        Tooltip(self.btn_new, "Ctrl+N")
        window.bind("<Control-n>", lambda event: self.btn_new.invoke())
        
        Tooltip(self.btn_close, "Ctrl+Alt+C")
        window.bind("<Control-Alt-c>", lambda event: self.btn_close.invoke())   

        Tooltip(self.btn_browse, "Ctrl+B")
        window.bind("<Control-b>", lambda event: self.btn_browse.invoke())

        Tooltip(self.txt_search, "Ctrl+F")
        window.bind("<Control-f>", lambda event: self.txt_search.focus())
        # -----------------------------------------------

        # setup placeholder text ------------------------
        self.init_placeholder(self.txt_email, ("example12@gmail.com"))
        self.init_placeholder(self.txt_search, ("Search By Name"))



        # Load Data Gridview
        self.load_grid()

        # tooltip for image
        self.tooltip = CreateImageToolTip(self.window, self.tree)


    def validate_input(self, text, val):
        for char in text:
            if not char.isdigit():
                return False
            else:
                if int(text) >= int(val):
                    return False
        return True

    def frm_control(self):
        self.lbl_header = Label(
            self.frame_head,
            text="Student Information",
            font=("Courier New", 18, "bold"),
            bg="#739072",
            fg="#F0F0F0",
        )
        self.lbl_header.pack(pady=5, anchor="center")
        self.lbl_id = Label(
            self.frm_1, text="ID :", font=("Courier New", 12, "bold"), bg="#B0D9B1"
        )
        self.lbl_id.pack(side="left", padx=5, pady=5, anchor="w")

        self.txt_id = Entry(
            self.frm_1, width=25, justify="center", font=("Courier New", 12, "bold")
        )
        self.txt_id.pack(side="right", padx=5, pady=5, anchor="e")
        self.txt_id["state"] = "readonly"


        # Name -----------------------------------------
        self.lbl_name = Label(
            self.frm_2, text="Name :", font=("Courier New", 12, "bold"), bg="#B0D9B1"
        )
        self.lbl_name.pack(side="left", padx=5, pady=5, anchor="w")

        self.txt_name = AutocompleteEntry(self.frm_2, completevalues=self.name, width=25, justify="center", font=("Courier New", 12, "bold"))
        self.txt_name.pack(side="right", padx=5, pady=5, anchor="e")
        # Bind Focus In and Focus Out -------------------
        self.txt_name.bind(
            "<FocusIn>", lambda event, entry=self.txt_name: entry.config(bg="#FFFB73")
        )
        self.txt_name.bind(
            "<FocusOut>", lambda event, entry=self.txt_name: entry.config(bg="white")
        )
        # Bind Enter Key  to move to next widget --------
        self.txt_name.bind(
            "<Return>", lambda event, entry=self.txt_name: entry.tk_focusNext().focus()
        )

        # ------------------------------------------------

        self.lbl_gender = Label(
            self.frm_3, text="Gender :", font=("Courier New", 12, "bold"), bg="#B0D9B1"
        )
        self.lbl_gender.pack(side="left", padx=5, pady=5, anchor="w")

        self.cmb_gender = ttk.Combobox(
            self.frm_3, width=23, justify="center", font=("Courier New", 12, "bold")
        )
        self.cmb_gender.pack(side="right", padx=5, pady=5, anchor="e")
        self.cmb_gender["values"] = ["Male", "Female", "Other"]
        self.cmb_gender["state"] = "readonly"
        # Bind Enter Key  to move to next widget --------
        self.cmb_gender.bind(
            "<Return>",
            lambda event, entry=self.cmb_gender: entry.tk_focusNext().focus(),
        )

        # ------------------------------------------------
        self.lbl_contact_number = Label(
            self.frm_4,
            text="Contact Number :",
            font=("Courier New", 12, "bold"),
            bg="#B0D9B1",
        )
        self.lbl_contact_number.pack(side="left", padx=5, pady=5, anchor="w")

        self.txt_contact_number = Entry(
            self.frm_4,
            width=25,
            justify="center",
            font=("Courier New", 12, "bold"),
            validate="key",
        )
        self.txt_contact_number.pack(side="right", padx=5, pady=5, anchor="e")
        # Bind Focus In and Focus Out -------------------
        self.txt_contact_number.bind(
            "<FocusIn>",
            lambda event, entry=self.txt_contact_number: entry.config(bg="#FFFB73"),
        )
        self.txt_contact_number.bind(
            "<FocusOut>",
            lambda event, entry=self.txt_contact_number: entry.config(bg="white"),
        )
        # Bind Enter Key  to move to next widget --------
        self.txt_contact_number.bind(
            "<Return>",
            lambda event, entry=self.txt_contact_number: entry.tk_focusNext().focus(),
        )

        # ------------------------------------------------
        self.lbl_email = Label(
            self.frm_5, text="Email :", font=("Courier New", 12, "bold"), bg="#B0D9B1"
        )
        self.lbl_email.pack(side="left", padx=5, pady=5, anchor="w")

        self.txt_email = Entry(
            self.frm_5, width=25, justify="center", font=("Courier New", 12, "bold"), 
        )
        self.txt_email.pack(side="right", padx=5, pady=5, anchor="e")
        
        # Bind Focus In and Focus Out -------------------
        self.txt_email.bind(
            "<FocusIn>", lambda event, entry=self.txt_email: entry.config(bg="#FFFB73")
        )
        self.txt_email.bind(
            "<FocusOut>", lambda event, entry=self.txt_email: entry.config(bg="white")
        )
        # Bind Enter Key  to move to next widget --------
        self.txt_email.bind(
            "<Return>", lambda event, entry=self.txt_email: entry.tk_focusNext().focus()
        )

        # ------------------------------------------------
        self.lbl_date_of_birth = Label(
            self.frm_6,
            text="Date of Birth f'dd/mm/YYYY ",
            font=("Courier New", 12, "bold"),
            bg="#B0D9B1",
        )
        self.lbl_date_of_birth.pack(side="left", padx=5, pady=5, anchor="w")

        self.txt_day = Entry(
            self.frm_10,
            width=3,
            justify="center",
            font=("Courier New", 12, "bold"),
            validate="key",
        )
        self.txt_day.pack(side="left", padx=5, pady=5, fill="none")
        # Bind Focus In and Focus Out -------------------
        self.txt_day.bind(
            "<FocusIn>", lambda event, entry=self.txt_day: entry.config(bg="#FFFB73")
        )
        self.txt_day.bind(
            "<FocusOut>", lambda event, entry=self.txt_day: entry.config(bg="white")
        )
        # Bind Enter Key  to move to next widget --------
        self.txt_day.bind(
            "<Return>", lambda event, entry=self.txt_day: entry.tk_focusNext().focus()
        )

        # Use of Slash to visually separate the date
        self.lbl_first_slash = Label(
            self.frm_10, text="/", font=("Courier New", 12, "bold"), bg="#B0D9B1"
        )
        self.lbl_first_slash.pack(side="left", padx=5, pady=5, anchor="w", fill="none")

        self.txt_month = Entry(
            self.frm_10,
            width=3,
            justify="center",
            font=("Courier New", 12, "bold"),
            validate="key",
        )
        self.txt_month.pack(side="left", padx=5, pady=5, fill="none")
        # Bind Focus In and Focus Out -------------------
        self.txt_month.bind(
            "<FocusIn>", lambda event, entry=self.txt_month: entry.config(bg="#FFFB73")
        )
        self.txt_month.bind(
            "<FocusOut>", lambda event, entry=self.txt_month: entry.config(bg="white")
        )
        # Bind Enter Key  to move to next widget --------
        self.txt_month.bind(
            "<Return>", lambda event, entry=self.txt_month: entry.tk_focusNext().focus()
        )

        # Use of Slash to visually separate the date
        self.lbl_second_slash = Label(
            self.frm_10, text="/", font=("Courier New", 12, "bold"), bg="#B0D9B1"
        )
        self.lbl_second_slash.pack(side="left", padx=5, pady=5, anchor="w", fill="none")
        self.txt_year = Entry(
            self.frm_10,
            width=5,
            justify="center",
            font=("Courier New", 12, "bold"),
            validate="key",
        )
        self.txt_year.pack(side="left", padx=5, pady=5, fill="none")
        # Bind Focus In and Focus Out -------------------
        self.txt_year.bind(
            "<FocusIn>", lambda event, entry=self.txt_year: entry.config(bg="#FFFB73")
        )
        self.txt_year.bind(
            "<FocusOut>", lambda event, entry=self.txt_year: entry.config(bg="white")
        )
        # Bind Enter Key  to move to next widget --------
        self.txt_year.bind(
            "<Return>", lambda event, entry=self.txt_year: entry.tk_focusNext().focus()
        )

        # Search ---------------------------------------
        self.txt_search = Entry(
            self.frm_12, width=20, justify="center", font=("Courier New", 12, "bold")
        )
        self.txt_search.pack(side="right", padx=5, pady=5, anchor="e")
        # Bind Focus In and Focus Out -------------------
        self.txt_search.bind("<FocusIn>", lambda event, entry=self.txt_day: entry.config(bg="#FFFB73"))
        self.txt_search.bind(
            "<FocusOut>", lambda event, entry=self.txt_search: entry.config(bg="white")
        )


        self.txt_search.bind("<KeyRelease>", lambda event: self.on_search(event))



        # Open Default Image ----------------------------
        self.img = Image.open("./resource/unicorn.png")
        self.img = self.img.resize((130, 140))
        self.pic_box = ImageTk.PhotoImage(self.img)

        self.lbl_pic_box = Label(self.frm_7, image=self.pic_box, width=130, height=140)
        self.lbl_pic_box.pack(side="top", padx=5, pady=5, anchor="e")
        # -----------------------------------------------

        # Button Browse for Image -----------------------
        self.btn_browse = Button(
            self.frm_7,
            text="Browse",
            font=("Courier New", 12, "bold"),
            bg="#CEE9D6",
            border=2,
            width=10,
            height=1,
            activebackground="#F1B763",
            command=lambda: self.browse_image(),
        )
        self.btn_browse.pack(side="top", padx=5, pady=5, anchor="center")
        # -----------------------------------------------

        # ---- Button Control ----------------------------
        self.btn_new = Button(
            self.frm_btn,
            text="New",
            font=("Courier New", 12, "bold"),
            bg="#CEE9D6",
            border=2,
            width=10,
            height=1,
            justify="center",
            activebackground="#F1B763",
            command=lambda: self.new_reset(),
        )
        self.btn_new.grid(column=1, row=1, sticky="ew", padx=7, pady=7)
        self.btn_new.bind("<return>")

        # ---- Button Save
        self.btn_save = Button(
            self.frm_btn,
            text="Save",
            font=("Courier New", 12, "bold"),
            bg="#CEE9D6",
            border=2,
            width=10,
            height=1,
            justify="center",
            activebackground="#F1B763",
            command=lambda: self.insert_data(),
        )
        self.btn_save.grid(column=1, row=2, sticky="ew", padx=7, pady=7)

        self.btn_update = Button(
            self.frm_btn,
            text="Update",
            font=("Courier New", 12, "bold"),
            bg="#CEE9D6",
            border=2,
            width=10,
            height=1,
            justify="center",
            activebackground="#F1B763",
            command=lambda: self.update_data(),
        )
        self.btn_update.grid(column=1, row=3, sticky="ew", padx=7, pady=7)

        self.btn_close = Button(
            self.frm_btn,
            text="Close",
            font=("Courier New", 12, "bold"),
            bg="#CEE9D6",
            border=2,
            width=10,
            height=1,
            justify="center",
            activebackground="#F1B763",
            command=lambda: self.close_app(),
        )
        self.btn_close.grid(column=1, row=4, sticky="ew", padx=7, pady=7)

        # Add Treeview as data gridview
        self.tree = ttk.Treeview(
            self.frame_grid,
            columns=(
                "Student ID",
                "Student Name",
                "Gender",
                "Contact Number",
                "Email",
                "Date of Birth",
            ),
            height=15,
            show="headings",
            selectmode="extended",
        )
        # Define column heading and set width
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Student Name", text="Student Name")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Contact Number", text="Contact Number")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Date of Birth", text="Date of Birth")

        self.tree.column(
            "Student ID", width=100, anchor="center", stretch=True
        )  # Set Width of column 2 to 150 pixels
        self.tree.column(
            "Student Name", width=200, anchor="center", stretch=True
        )  # Set width of column 3 to 200 pixels
        self.tree.column(
            "Contact Number", width=150, anchor="center", stretch=True
        )  # Set width of column 4 to 100 pixels
        self.tree.column("Email", width=200, anchor="center", stretch=True)
        self.tree.column("Date of Birth", width=150, anchor="center", stretch=True)

        # Add Vertical and Horizontal Scrollbar
        treeYScroll = ttk.Scrollbar(self.frame_grid, orient="vertical")
        treeYScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeYScroll.set)
        treeYScroll.pack(side="right", fill="y")

        treeXScroll = ttk.Scrollbar(self.frame_grid, orient="horizontal")
        treeXScroll.configure(command=self.tree.xview)
        self.tree.configure(xscrollcommand=treeXScroll.set)
        treeXScroll.pack(side="bottom", fill="x")

        self.tree.pack(side="bottom", fill="both", anchor="s")
        self.tree.bind("<Button-3>", lambda event: self.show_content_menu(event=event))  # Bind Right Click to Treeview

        # Bing tooltip image to treeview
        self.tree.bind("<Button-1>", lambda event: self.on_mouse_over(event))
        self.tree.bind("<ButtonRelease-1>", lambda event: self.on_mouse_leave(event))

    # SQLlite Database ---------------------------------
        
    def insert_data(self):
        
        
        if self.txt_name.get() == '':
            tmsg.showerror("Error", "Please Enter Name")
            self.txt_name.focus()
            return
        if self.cmb_gender.get() == '':
            tmsg.showerror('Error','Please Select Gender')
            self.cmb_gender.focus()
            return
        if self.txt_contact_number.get() == '':
            tmsg.showerror('Error','Please Enter Contact Number')
            self.txt_contact_number.focus()
            return
        if self.txt_email.get() == 'example12@gmail.com':
            self.txt_email.delete(0, "end")
        else:
            if not re.match(EMAIL_REGEX, self.txt_email.get()):
                tmsg.showerror('Error','Please Enter Valid Email')
                self.txt_email.focus()
                return
        if self.txt_day.get() == '' or self.txt_month.get() == '' or self.txt_year.get() == '':
            tmsg.showerror('Error','Please Enter Date of Birth')
            self.txt_day.focus()
            return  
        else:
            try:
                str_date = self.txt_day.get() + "/" + self.txt_month.get() + "/" + self.txt_year.get()
                datetime.strptime(str_date, '%d/%m/%Y')
            except ValueError:
                tmsg.showerror('Error','Please Enter Valid Date')
                self.txt_day.focus()
                return
        try:   
            if hasattr(self.lbl_pic_box, "image"):
                name = self.txt_name.get()
                gend = self.cmb_gender.get()
                cont = self.txt_contact_number.get()
                email = self.txt_email.get()
                conn = sqlite3.connect('resource/data/stu_info.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO std_details VALUES (NULL,?,?,?,?,?)", (name, gend, cont, email, str_date))
                conn.commit()
                inserted_id = cursor.lastrowid                
                conn.close()

                img_tk = self.lbl_pic_box.image
                img = ImageTk.getimage(img_tk)
                img = img.convert("RGB")
                save_path = "./resource/image/" + str(inserted_id) + ".jpg"
                img.save(save_path, "JPEG")
                tmsg.showinfo("Success", "Data Inserted Successfully")
                # Load Data Gridview
                self.load_grid()
                self.btn_new.invoke()
            else:
                name = self.txt_name.get()
                gend = self.cmb_gender.get()
                cont = self.txt_contact_number.get()
                email = self.txt_email.get()

                conn = sqlite3.connect('resource/data/stu_info.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO std_details VALUES (NULL,?,?,?,?,?)", (name, gend, cont, email, str_date))
                conn.commit()
                inserted_id = cursor.lastrowid
                conn.close()
                tmsg.showinfo("Success", "Data Inserted Successfully")
                # Load Data Gridview
                self.load_grid()

                self.btn_new.invoke()  #Last Update Video 21:24 
        except Exception as e:
            tmsg.showerror("Error", f"Insert Error due to {str(e)}")

    def load_grid(self):
        try:
            conn = sqlite3.connect('./resource/data/stu_info.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Id, name, gen, contact, email, det FROM std_details")
            # fetch all data from database
            self.data = cursor.fetchall()
            conn.close()
            self.tree.delete(*self.tree.get_children())
            for row in self.data:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            tmsg.showerror("Error", f"Load Grid Error due to {str(e)}")

    def load_autocomplete(self):
        try:
            conn = sqlite3.connect('./resource/data/stu_info.db')
            cursor = conn.cursor()
            sql_query = "SELECT DISTINCT name FROM std_details"
            cursor.execute(sql_query)
            # fetch all data from database
            data = cursor.fetchall()
            conn.close()
            self.name = [item[0] for item in data]
        except Exception as e:
            tmsg.showerror("Error", f"from Autocomplete text: {str(e)}")

    def browse_image(self):
        self.file_path = filedialog.askopenfilename(
            title="Select A File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if self.file_path:
            img = Image.open(self.file_path)
            img = img.resize((130, 140))
            img_tk = ImageTk.PhotoImage(img)
            self.lbl_pic_box.configure(image=img_tk)
            self.lbl_pic_box.image = img_tk

    def new_reset(self):

        try:
            # Reset all text fields
            self.txt_id.configure(state="normal")
            self.txt_id.delete(0, "end")
            self.txt_id.configure(state="readonly")

            self.txt_name.delete(0, "end")
            self.cmb_gender.set("")

            self.txt_contact_number.delete(0, "end")
            
            self.txt_email.delete(0, "end")
            self.init_placeholder(self.txt_email, ("example12@gmail.com"))
            
            self.txt_day.delete(0, "end")
            self.txt_month.delete(0, "end")
            self.txt_year.delete(0, "end")
            
            self.txt_search.delete(0, "end")            
            self.init_placeholder(self.txt_search, ("Search Everything"))

            # Reset Image
            img = Image.open("./resource/unicorn.png")
            img = self.img.resize((130, 140))
            img_tk = ImageTk.PhotoImage(img)
            self.lbl_pic_box.image = img_tk
            self.lbl_pic_box.configure(image=img_tk)

            self.txt_name.focus()

        except Exception as e:
            tmsg.showerror("Error", f"new reset Error due to {str(e)}")

    def show_content_menu(self, event):  # It will be binded to treeview
        
        # Get the item selected under the cursor
        try:
            item = self.tree.item(self.tree.focus())
            if item:
                self.content_menu.post(event.x_root, event.y_root)
        except Exception as e:
            tmsg.showerror("Error", f"show content menu Error due to {str(e)}")

    def edit_item(self):
        try:
           item = self.tree.selection() # Get values of the select item
           if not item:
                tmsg.showerror("Error", "Please Select row to Edit")
                return
           else:
                values = self.tree.item(item,"values")
                self.txt_id.configure(state="normal")
                self.txt_id.delete(0, "end")
                self.txt_id.insert(0, values[0])
                self.txt_id.config(state="readonly")
                self.txt_name.delete(0, "end")
                self.txt_name.insert(0, values[1])
                self.cmb_gender.set("")
                self.cmb_gender.set(values[2])
                self.txt_contact_number.delete(0, "end")
                self.txt_contact_number.insert(0, values[3])
                self.txt_email.delete(0, "end")
                if values[4] == "":
                    self.init_placeholder(self.txt_email, ("example12@gmail.com"))
                else:
                    self.txt_email.insert(0, values[4])
                    date = values[5]

                    self.txt_day.delete(0, "end")
                    self.txt_day.insert(0, date[0:2])
                    self.txt_month.delete(0, "end")
                    self.txt_month.insert(0, date[3:5])
                    self.txt_year.delete(0, "end")
                    self.txt_year.insert(0, date[6:])
                    imag_path = f"./resource/image/{values[0]}.jpg"
                    if os.path.exists(imag_path):
                        img = Image.open(imag_path)
                        img = img.resize((130, 140))
                        img_tk = ImageTk.PhotoImage(img)
                        self.lbl_pic_box.image = img_tk
                        self.lbl_pic_box.configure(image=img_tk)
                    else:
                        tmsg.showwarning("Warning", "Image not found")
                        # img = Image.open("./resource/unicorn.png")
                        # img = img.resize((130, 140))
                        # img_tk = ImageTk.PhotoImage(img)
                        # self.lbl_pic_box.image = img_tk
                        # self.lbl_pic_box.configure(image=img_tk)
        except Exception as e:
            tmsg.showerror("Error", f"from retrieve {str(e)}")


                

               



        except Exception as e:
            tmsg.showerror("Error", f"Edit Error due to {str(e)}")

    def update_data(self):
         
        if self.txt_name.get() == '':
            tmsg.showerror("Error", "Please Enter Name")
            self.txt_name.focus()
            return
                           
        if self.cmb_gender.get() == '':
            tmsg.showerror('Error','Please Select Gender')
            self.cmb_gender.focus()
            return
        
        if self.txt_contact_number.get() == '':
            tmsg.showerror('Error','Please Enter Contact Number')
            self.txt_contact_number.focus()
            return
        if self.txt_email.get() == 'example12@gmail.com':
            self.txt_email.delete(0, "end")
        else:
            if not re.match(EMAIL_REGEX, self.txt_email.get()):
                tmsg.showerror('Error','Please Enter Valid Email')
                self.txt_email.focus()
                return
        if self.txt_day.get() == '' or self.txt_month.get() == '' or self.txt_year.get() == '':
            tmsg.showerror('Error','Please Enter Date of Birth')
            self.txt_day.focus()
            return  
        else:
            try:
                str_date = self.txt_day.get() + "/" + self.txt_month.get() + "/" + self.txt_year.get()
                datetime.strptime(str_date, '%d/%m/%Y')
            except ValueError:
                tmsg.showerror('Error','Please Enter Valid Date')
                self.txt_day.focus()
                return
            
        
        try:   
            if hasattr(self.lbl_pic_box, "image"):
                self.txt_id.configure(state="normal")
                id = self.txt_id.get()
                self.txt_id.configure(state="readonly")

                name = self.txt_name.get()
                gend = self.cmb_gender.get()
                cont = self.txt_contact_number.get()
                email = self.txt_email.get()
                
                d = self.txt_day.get()
                m = self.txt_month.get()
                y = self.txt_year.get()
                str_date = d + "/" + m + "/" + y

                conn = sqlite3.connect('resource/data/stu_info.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE std_details SET name = ?, gen = ?, contact = ?, email = ?, det = ? WHERE Id = ?", (name, gend, cont, email, str_date, id))
                
                conn.commit()
                conn.close()
                
               

                # Image Update
                img_tk = self.lbl_pic_box.image
                img = ImageTk.getimage(img_tk)
                img = img.convert("RGB")
                # Specify the path to save the image
                save_path = "./resource/image/" + id + ".jpg"
                img.save(save_path, "JPEG")
                tmsg.showinfo("Success", "Data Updated Successfully")
                self.load_grid()
                self.btn_new.invoke()

            else:
                self.txt_id.configure(state="normal")
                id = self.txt_id.get()
                self.txt_id.configure(state="readonly")

                name = self.txt_name.get()
                gen = self.cmb_gender.get()
                cont = self.txt_contact_number.get()
                email = self.txt_email.get()
                d = self.txt_day.get()
                m = self.txt_month.get()
                y = self.txt_year.get()
                str_date = d + "/" + m + "/" + y

                conn = sqlite3.connect('resource/data/stu_info.db')
                cursor = conn.cursor()
                
                cursor.execute("UPDATE std_details SET name = ?, gen = ?, contact = ?, email = ?, det = ? WHERE Id = ?", (name, gen, cont, email, str_date, id))    
                conn.commit()
                conn.close()
                tmsg.showinfo("Success", "Data Updated Successfully")
                self.load_grid()
                self.btn_new.invoke()
        except Exception as e:
            tmsg.showerror("Error", f"Update Error due to {str(e)}")
                

            

        except Exception as e:
            tmsg.showerror("Error", f"Insert Error due to {str(e)}")

    def delete_item(self):
        try:
            item = self.tree.selection() # Get values of the select item
            if not item:
                tmsg.showwarning("Warning", "Please Select row to Delete")
                return
            # Confrmation to delete
            confirmation = tmsg.askyesno("Confirmation", "Do you want to delete this record?")
            if confirmation:

                values = self.tree.item(item,"values")
                conn = sqlite3.connect('resource/data/stu_info.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM std_details WHERE Id = ?", (values[0],))
                conn.commit()
                conn.close()
                
                imgae_file = f"./resource/image/{values[0]}.jpg"
                if os.path.exists(imgae_file):
                    os.remove(imgae_file)
                # Refresh Data Gridview
                self.load_grid()

                tmsg.showinfo("Success", "Data Deleted Successfully")
                

        except Exception as e:
            tmsg.showerror("Error", f"Delete Error due to {str(e)}")

    def on_search(self, event):
        try:
            search_query = self.txt_search.get()
            self.tree.delete(*self.tree.get_children())

            if not search_query:
                self.load_grid()
            else:
                # filter and insert matching rows into the Treeview
                filter_data = [(Id, name, gen, contact, email, det) for Id, name, gen, contact, email, det in self.data if search_query.lower() in name.lower()]
                for data in filter_data:
                    self.tree.insert("", "end", values=data)

        except Exception as e:
            tmsg.showerror("Error", f"on_search Error due to {str(e)}")

    def on_mouse_over(self, event):
        try:
            item = self.tree.identify_row(event.y)
            self.tooltip.show_tooltip(item, event)
        except Exception as e:
            tmsg.showerror("Error", f"on_mouse_over Error due to {str(e)}")

    def on_mouse_leave(self, event):
        try:
            self.tooltip.hide_tooltip()
        except Exception as e:
            tmsg.showerror("Error", f"on_mouse_leave Error due to {str(e)}")

    def close_app(self):
        try:
            confirmation = tmsg.askyesno("Confirmation", "Do you want to close this application?")
            if confirmation:
                self.window.destroy()
        except Exception as e:
            tmsg.showerror("Error", f"close_app Error due to {str(e)}")

if __name__ == "__main__":
    window = Tk()
    app = Myapp(window)
    window.mainloop()
