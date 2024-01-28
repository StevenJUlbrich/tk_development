from tkinter import ttk, Menu
import tkinter as tk
import os
from tkinter import messagebox as tsmg
from tkinter import Tk, Frame, Label, Entry, Button, StringVar, OptionMenu
from PIL import Image, ImageTk
import re
from datetime import datetime
from tkinter import filedialog
import sqlite3


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
        label = ttk.Label(self.tooltip, text= self.text, background="#FFFFDD", relief="solid", borderwidth=1, font=("TkDefaultFont", 10, "bold"))
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


        


class Myapp:
    def __init__(self, window):
        super().__init__()
        self.window = window
        window.title("Student Info")
        f_w = 1280
        f_h = 720
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

        self.frm_control()
        
        Tooltip(self.btn_save, "Ctrl+S")
        Tooltip(self.btn_update, "Ctrl+U")
        Tooltip(self.btn_new, "Ctrl+N")
        Tooltip(self.btn_close, "Ctrl+Alt+C")
        Tooltip(self.btn_browse, "Ctrl+B")


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

        self.lbl_name = Label(
            self.frm_2, text="Name :", font=("Courier New", 12, "bold"), bg="#B0D9B1"
        )
        self.lbl_name.pack(side="left", padx=5, pady=5, anchor="w")

        self.txt_name = Entry(
            self.frm_2, width=25, justify="center", font=("Courier New", 12, "bold")
        )
        self.txt_name.pack(side="right", padx=5, pady=5, anchor="e")
        self.txt_name.bind("<FocusIn>", lambda event, entry =self.txt_name: entry.config(bg="#FFFB73"))
        self.txt_name.bind("<FocusOut>", lambda event, entry =self.txt_name: entry.config(bg="white"))

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

        # ------------------------------------------------
        self.lbl_email = Label(
            self.frm_5, text="Email :", font=("Courier New", 12, "bold"), bg="#B0D9B1"
        )
        self.lbl_email.pack(side="left", padx=5, pady=5, anchor="w")

        self.txt_email = Entry(
            self.frm_5, width=25, justify="center", font=("Courier New", 12, "bold")
        )
        self.txt_email.pack(side="right", padx=5, pady=5, anchor="e")

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

        self.text_search = Entry(
            self.frm_12, width=20, justify="center", font=("Courier New", 12, "bold")
        )
        self.text_search.pack(side="right", padx=5, pady=5, anchor="e")

        self.img = Image.open("./resource/unicorn.png")
        self.img = self.img.resize((130, 140))
        self.pic_box = ImageTk.PhotoImage(self.img)

        self.lbl_pic_box = Label(self.frm_7, image=self.pic_box, width=130, height=140)
        self.lbl_pic_box.pack(side="top", padx=5, pady=5, anchor="e")

        self.btn_browse = Button(
            self.frm_7,
            text="Browse",
            font=("Courier New", 12, "bold"),
            bg="#CEE9D6",
            border=2,
            width=10,
            height=1,
            activebackground="#F1B763",
        )
        self.btn_browse.pack(side="top", padx=5, pady=5, anchor="center")

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
        )
        self.btn_new.grid(column=1, row=1, sticky="ew", padx=7, pady=7)
        self.btn_new.bind("<return>")

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

        treeYScroll = ttk.Scrollbar(self.frame_grid, orient="vertical")
        treeYScroll.configure(command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeYScroll.set)
        treeYScroll.pack(side="right", fill="y")

        treeXScroll = ttk.Scrollbar(self.frame_grid, orient="horizontal")
        treeXScroll.configure(command=self.tree.xview)
        self.tree.configure(xscrollcommand=treeXScroll.set)
        treeXScroll.pack(side="bottom", fill="x")

        self.tree.pack(side="bottom", fill="both", anchor="s")


if __name__ == "__main__":
    window = Tk()
    app = Myapp(window)
    window.mainloop()
