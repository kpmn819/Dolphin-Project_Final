#!/usr/bin/python
''' program to allow easy editing of the qna_pool.csv file that
    contains the questions and answers for game2'''

import tkinter as tk
from tkinter import DISABLED, IntVar, filedialog, messagebox, ttk
import csv
import os
from tkinter.font import NORMAL
import pandas as pd


#file_path = os.getcwd() + '/MyCode/qna_pool.csv'
file_path = '/home/pi/My-Code/Dolphin-Project/qna_pool.csv'
print(file_path)
# initalise the tkinter GUI
root = tk.Tk()

root.geometry("1500x800") # set the root dimensions
root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
root.resizable(0, 0) # makes the root window fixed in size.

# Frame for TreeView
frame1 = tk.LabelFrame(root, text="Questions and Answers")
frame1.place(height=500, width=1500)

# Frame for Editing Options dialog
file_frame = tk.LabelFrame(root, text="Editing Options")
file_frame.place(height=100, width=1000, rely=0.8, relx=0.15)

# Frame for data entry
entry_frame = tk.LabelFrame(root, text="Data Entry")
entry_frame.place(height=100, width=1000, rely=0.65, relx=0.15)

# Buttons
button_rely = 0.4
button2 = tk.Button(file_frame, text="Load File", command=lambda: Load_excel_data())
button2.place(rely=button_rely, relx= 0.02)

button1 = tk.Button(file_frame, text="Save File", command=lambda: save_file())
button1.place(rely=button_rely, relx= 0.12)
button1['state'] = tk.DISABLED # cause auto save is on

button3 = tk.Button(file_frame, text="Update Question", command=lambda: update_tree())
button3.place(rely=button_rely, relx= 0.24)

button4 = tk.Button(file_frame, text="Add Question", command=lambda: add_question())
button4.place(rely=button_rely, relx= 0.40)

button5 = tk.Button(file_frame, text="Delete Question", command=lambda: delete_question())
button5.place(rely=button_rely, relx= 0.55)

button6 = tk.Button(file_frame, text="Clear Entries", command=lambda: clear_entries())
button6.place(rely=button_rely, relx= 0.72)

auto = IntVar()
# check box
t1 = tk.Checkbutton(file_frame, text='Auto Save', variable=auto, onvalue=1, offvalue=0, command=lambda: auto_save())
t1.pack()
t1.select()

# The file/file path text
label_file = ttk.Label(file_frame, text="qna_pool.csv")
label_file.place(rely=0, relx=0)


# place edit fields
entry_width = 80
qu_label = tk.Label(entry_frame, text='Questions')
qu_label.grid(row=0, column=0, padx=10, pady=10)
qu_entry = tk.Entry(entry_frame)
qu_entry.grid(row=0, column=1,padx=10,pady=10,ipadx=entry_width)

ra_label = tk.Label(entry_frame, text='Correct')
ra_label.grid(row=0, column=3, padx=10, pady=10)
ra_entry = tk.Entry(entry_frame)
ra_entry.grid(row=0, column=4,padx=10,pady=10,ipadx=entry_width)

wa_label = tk.Label(entry_frame, text='Wrong A')
wa_label.grid(row=1, column=0, padx=10, pady=10)
wa_entry = tk.Entry(entry_frame)
wa_entry.grid(row=1, column=1,padx=10,pady=10,ipadx=entry_width)

wb_label = tk.Label(entry_frame, text='Wrong B')
wb_label.grid(row=1, column=3, padx=10, pady=10)
wb_entry = tk.Entry(entry_frame)
wb_entry.grid(row=1, column=4,padx=10,pady=10,ipadx=entry_width)

# Treeview Widget
tv1 = ttk.Treeview(frame1)
tv1.place(relheight=.9, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget


def File_dialog():
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    # not used in this version of code but handy to keep around
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
    label_file["text"] = filename
    
    return None
    

def Load_excel_data():
    """If the file selected is valid this will load the file into the Treeview"""
    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)
        else:
            df = pd.read_excel(excel_filename)

    except ValueError:
        tk.messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        tk.messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    clear_data()
    tv1["column"] = list(df.columns)
    tv1["show"] = "headings"
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name
        tv1.column(column, width= 350)

    df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see 
        # https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
    return None

def auto_save():
    if auto.get():
        button1['state'] = tk.DISABLED
    else:
        button1['state'] = tk.NORMAL

 
    print('auto value '+ str(auto.get()))

def save_file():
    print('saving file')
    #csv_file = open("qna_pool.csv", "w")
    csv_file = open(file_path, "w")

	# put in the header
    csv_file.write('question'+','+'right answer'+','+'wrong a'+','+'wrong b')
    csv_file.write('\n')
    # now put in the lines of data
    for line in tv1.get_children():
        each_q = []
        #i = 0
        for value in tv1.item(line)['values']:
            each_q.append(value)
 
        # set up each q with linefeed
        csv_file.write(each_q[0] +','+each_q[1] +','+each_q[2] +','+each_q[3])
        csv_file.write('\n')
        csv_file.close	
	
    csv_file.close

def add_question():
    blanks = no_blanks()
    if blanks:
        print('blanks not allowed')
        messagebox.showerror('Blank Entry', 'Please enter data in blank field')
        return
    tv1.insert(parent='', index='end', text='', values=(qu_entry.get(), ra_entry.get(), wa_entry.get(), wb_entry.get()))
    clear_entries()
    if auto.get():
        save_file()

def delete_question():
    #print(str(tv1.focus()))
    tv1.delete(str(tv1.focus()))
    clear_entries()
    if auto.get():
        save_file()

def clear_data():
    tv1.delete(*tv1.get_children())
    return None

# Clear entry boxes
def clear_entries():
	# Clear entry boxes
	qu_entry.delete(0, tk.END)
	ra_entry.delete(0, tk.END)
	wa_entry.delete(0, tk.END)
	wb_entry.delete(0, tk.END)

# Select Record
def select_data(e):
	# Clear entry boxes
	qu_entry.delete(0, tk.END)
	ra_entry.delete(0, tk.END)
	wa_entry.delete(0, tk.END)
	wb_entry.delete(0, tk.END)


	# Grab record Number
	selected = tv1.focus()
	# Grab record values
	values = tv1.item(selected, 'values')

	# output to entry boxes
	qu_entry.insert(0, values[0])
	ra_entry.insert(0, values[1])
	wa_entry.insert(0, values[2])
	wb_entry.insert(0, values[3])

def update_tree():
    print('this will update the tree entries')
    no_commas() # make sure there are no commas
    # Don't let them get away with blanks
    blanks = no_blanks()
    if blanks:
        print('blanks not allowed')
        messagebox.showerror('Blank Entry', 'Please enter data in blank field')
        return
    selected = tv1.focus()
    # Update record
    tv1.item(selected, text="", values=(qu_entry.get(), ra_entry.get(), wa_entry.get(), wb_entry.get(),))
    if auto.get():
        save_file()

def no_commas():
    # filter out commas from entry boxes
    qu_org = qu_entry.get()
    qu_nc = qu_org.replace(',', '')
    if qu_org != qu_nc:
        qu_entry.delete(0, tk.END)
        qu_entry.insert(0, qu_nc)

    ra_org = ra_entry.get()
    ra_nc = ra_org.replace(',', '')
    if ra_org != ra_nc:
        ra_entry.delete(0, tk.END)
        ra_entry.insert(0, ra_nc)
    
    wa_org = wa_entry.get()
    wa_nc = wa_org.replace(',', '')
    if wa_org != wa_nc:
        wa_entry.delete(0, tk.END)
        wa_entry.insert(0, wa_nc)
    
    wb_org = wb_entry.get()
    wb_nc = wb_org.replace(',', '')
    if wb_org != wb_nc:
        wb_entry.delete(0, tk.END)
        wb_entry.insert(0, wb_nc)

def no_blanks():
    blanks = False
    if qu_entry.get() == '':
        blanks = True
    if ra_entry.get() == '':
        blanks = True
    if wa_entry.get() == '':
        blanks = True
    if wb_entry.get() == '':
        blanks = True
    return blanks   

tv1.bind("<ButtonRelease-1>", select_data)

root.mainloop()