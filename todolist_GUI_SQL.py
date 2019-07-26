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


def time_input(the_time):
    split_time = the_time.split(":")
    try:
        # validate the time format within range 00:00 and 23:59
        if int(split_time[1]) > 59 or int(split_time[1]) < 0 or int(split_time[0]) > 23 or int(split_time[0]) < 0:
            messagebox.showerror("time entry error", "incorrect number")
            return
    except Exception:
        print(the_time)
        messagebox.showerror("time entry error", "wrong input string format")
        return 0

    return the_time


def add_to_list():
    time = time_input(addTime.get())
    des = addDes.get()

    # make sure that all entry is not empty
    if (len(selected_priority[0]) is not 0) or time != 0 or (len(des) is not 0):
        cursor.execute("INSERT INTO listTable(level, time, desc) Values(?,?,?)", (selected_priority[0], time, des))
        messagebox.showinfo("Update", "task has been added!")
        addTime.delete(0, "end")
        addDes.delete(0, "end")
        right_frame.destroy()
        show_list()

    else:
        messagebox.showinfo("Entry Error", "Entry Error!")
    connection.commit()


def show_list():
    global right_frame
    right_frame = tk.Frame(mainFrame)
    right_frame.grid(row=0, column=1)

    # showing the lists
    tk.Label(right_frame, text="Priority", padx=10).grid(row=0, column=0)
    tk.Label(right_frame, text="Time", padx=10).grid(row=0, column=1)
    tk.Label(right_frame, text="Description", padx=10, justify=tk.LEFT).grid(row=0, column=2)

    cursor.execute("SELECT level, time, desc FROM listTable")
    task_list = cursor.fetchall()
    # database is empty
    if len(task_list) is 0:
        tk.Label(right_frame, text="Database is empty!").grid(row=1, column=1)

    # record found
    else:
        count = 1
        for task in task_list:
            # each line have one task with type, time, and Description
            tk.Label(right_frame, text=task[0]).grid(row=count, column=0)
            tk.Label(right_frame, text=task[1]).grid(row=count, column=1)
            tk.Label(right_frame, text=task[2]).grid(row=count, column=2)

            # print("{}\t{}\t{}\n".format(task[0], task[1], task[2]))
            count = count+1

    def delete_task():
        time = time_input(delete_entry.get())
        if time == 0:
            return
        cursor.execute("DELETE FROM listTable WHERE time = \"{}\"".format(time))
        messagebox.showinfo("Update", "Database has been updated!")

        connection.commit()
        right_frame.destroy()
        show_list()

    delete_entry = tk.Entry(right_frame)
    delete_entry.grid(row=0, column=3)
    tk.Button(right_frame, text="Delete by Time", command=delete_task).grid(row=1, column=3)


def select_high():
    selected_priority[0] = "High"


def select_medium():
    selected_priority[0] = "Medium"


def select_low():
    selected_priority[0] = "Low"


mainFrame = tk.Tk()
mainFrame.title("To do list")
selected_priority = ["Low"]

left_frame = tk.Frame(mainFrame)
left_frame.grid(row=0, column=0)

right_frame = tk.Frame(mainFrame)

typeLabel = tk.Label(left_frame, text="Priority", justify=tk.RIGHT).grid(row=0, column=0)

select_type_frame = tk.Frame(left_frame)
select_type_frame.grid(row=0, column=1)
button_high = tk.Button(select_type_frame, text="High", command=select_high).grid(column=0, row=0)
button_medium = tk.Button(select_type_frame, text="Medium", command=select_medium).grid(column=1, row=0)
button_low = tk.Button(select_type_frame, text="Low", command=select_low).grid(column=2, row=0)


timeLabel = tk.Label(left_frame,  text="Time\n(00:00 - 23:59)").grid(row=1, column=0)
addTime = tk.Entry(left_frame)
addTime.grid(row=1, column=1)

desLabel = tk.Label(left_frame, text="Description", justify=tk.RIGHT).grid(row=2, column=0)
addDes = tk.Entry(left_frame)
addDes.grid(row=2, column=1)

addButton = tk.Button(left_frame, text="Add", command=add_to_list)
addButton.grid(row=3, column=1)

show_list()

mainFrame.mainloop()
