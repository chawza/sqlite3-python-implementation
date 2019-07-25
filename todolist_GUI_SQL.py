import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox

connection = sq.connect("ActivityDataBase.db")
cursor = connection.cursor()

try:
    cursor.execute("""CREATE TABLE listTable(
        level TEXT,
        time TEXT,
        desc TEXT
    );""")  # time activity is the KEY file

    messagebox.showinfo("information", "Database has been created!")

except:
    messagebox.showinfo("information", "Database found!")


def add_to_list():
    time = addTime.get()
    des = addDes.get()

    split_time = time.split(":")
    try:
        # validate the time format within range 00:00 and 23:59
        if int(split_time[1]) > 59 or int(split_time[1]) < 0 or int(split_time[0]) > 23 or int(split_time[0]) < 0:
            messagebox.showerror("time entry error", "incorrect number")
            return
    except:
        messagebox.showerror("time entry error", "wrong input string format")
        return

    # make sure that all entry is not empty
    if (len(selected_priority[0]) is not 0) or (len(time) is not 0) or (len(des) is not 0):
        cursor.execute("INSERT INTO listTable(level, time, desc) Values(?,?,?)", (selected_priority[0], time, des))
        messagebox.showinfo("Update", "task has been added!")
        addTime.delete(0, "end")
        addDes.delete(0, "end")

    else:
        messagebox.showinfo("Entry Error", "Entry Error!")
    connection.commit()


def show_list():
    # new child window
    list_frame = tk.Toplevel()
    list_frame.title("Activity List")

    # showing the lists
    tk.Label(list_frame, text="Priority").grid(row=0, column=1)
    tk.Label(list_frame, text="Time").grid(row=0, column=2)
    tk.Label(list_frame, text="Description").grid(row=0, column=3)

    cursor.execute("SELECT level, time, desc FROM listTable")
    task_list = cursor.fetchall()

    # database is empty
    if task_list is None:
        tk.Label(list_frame, text="Database is empty").grid(row=1, column=3)

    # record found
    else:
        count = 1
        for task in task_list:
            # each line have one task with type, time, and Description
            tk.Label(list_frame, text=task[0]).grid(row=count, column=1)
            tk.Label(list_frame, text=task[1]).grid(row=count, column=2)
            tk.Label(list_frame, text=task[2]).grid(row=count, column=3)

            # print("{}\t{}\t{}\n".format(task[0], task[1], task[2]))
            count = count+1

    # delete tasks from the tables
    def delete_task():
        try:
            cursor.execute("DELETE FROM listTable WHERE time = \"{}\"".format(delete_entry.get()))
            messagebox.showinfo("Update", "Database has been updated!")
            connection.commit()
            list_frame.destroy()
            show_list()

        except:
            messagebox.showerror("Entry Error", "Input is incorrect")
    tk.Label(list_frame, text="Select to Delete by time").grid(row=0, column=4)
    delete_entry = tk.Entry(list_frame)
    delete_entry.grid(row=1, column=4)
    tk.Button(list_frame, text="Delete", command=delete_task).grid(row=2, column=4)

    # dismiss button
    if count <= 2:
        count = 3
    tk.Button(list_frame, text="Dismiss", command=list_frame.destroy).grid(row=count, column=4)


def select_high():
    selected_priority[0] = "High"


def select_medium():
    selected_priority[0] = "Medium"


def select_low():
    selected_priority[0] = "Low"


mainFrame = tk.Tk()
mainFrame.title("To do list")
selected_priority = ["Low"]

# adding activity menu
typeLabel = tk.Label(mainFrame, text="Priority (High, Medium, Low)", justify=tk.RIGHT).grid(row=0, column=0)

select_type_frame = tk.Frame(mainFrame)
select_type_frame.grid(row=0, column=1)
button_high = tk.Button(select_type_frame, text="High", command=select_high).grid(column=0, row=0)
button_medium = tk.Button(select_type_frame, text="Medium", command=select_medium).grid(column=1, row=0)
button_low = tk.Button(select_type_frame, text="Low", command=select_low).grid(column=2, row=0)


timeLabel = tk.Label(mainFrame,  text="Time (00:00 - 23:59)", justify=tk.RIGHT).grid(row=1, column=0)
addTime = tk.Entry(mainFrame)
addTime.grid(row=1, column=1)

desLabel = tk.Label(mainFrame, text="Description", justify=tk.RIGHT).grid(row=2, column=0)
addDes = tk.Entry(mainFrame)
addDes.grid(row=2, column=1)

addButton = tk.Button(mainFrame, text="Add", command=add_to_list)
addButton.grid(row=3, column=1)


# below (the task list)
tk.Button(mainFrame, text="Show Activities", command=show_list).grid(row=4, column=0)


mainFrame.mainloop()
