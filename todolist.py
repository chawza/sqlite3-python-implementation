import sqlite3

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

cursor.execute("""CREATE TABLE listTable(
    level TEXT,
    time TEXT,
    desc TEXT
);""")  # time activity is the KEY file

def show_act(choice):
    if choice is "Y" or choice is "y":
        cursor.execute("SELECT * FROM listTable WHERE level = \"HIGH\"")
        for index, row in enumerate(cursor.fetchall(), start = 1):
            print("{}. Type: {}\tTime: {}\n   Description:\n   {}\n".format(index, row[0], row[1], row[2]))

        cursor.execute("SELECT * FROM listTable WHERE level = \"MEDIUM\"")
        for index, row in enumerate(cursor.fetchall(), start = 1):
            print("{}. Type: {}\tTime: {}\n   Description:\n   {}\n".format(index, row[0], row[1], row[2]))

        cursor.execute("SELECT * FROM listTable WHERE level = \"LOW\"")
        for index, row in enumerate(cursor.fetchall(), start = 1):
            print("{}. Type: {}\tTime: {}\n   Description:\n   {}\n".format(index, row[0], row[1], row[2]))
    else:    
        cursor.execute("SELECT * FROM listTable")
        for index, row in enumerate(cursor.fetchall(), start = 1):
            print("{}. Type: {}\tTime: {}\n   Description:\n   {}\n".format(index, row[0], row[1], row[2]))
    

def add_act(act_type, act_time, act_des):
    cursor.execute("INSERT INTO listTable VALUES(?, ?, ?)", (act_type, act_time, act_des))
    print("New Activity Has been Added!")
    connection.commit()


def del_act(time):
    cursor.execute("DELETE FROM listTable WHERE time = \"{}\"".format(time))
    print("Activity has been deleted!")
    connection.commit()


def print_blanks():
    for a in range(20):
        print("\n")


def set_time_input():
    while True:     # loop until return
        times = input("set time between 00:00 to 24:00: ")

        try:        # if user input wrong format!
            time = times.split(":")
            if int(time[0]) <= 24 and int(time[0]) >= 0 and int(time[1]) <= 60 and int(time[1]) >= 0:
                if int(time[0]) >= 24 and int(time[1]) > 0: #time cannot more than 24:00
                    print("time is not correct!\n")
                    continue
                else:
                    return times        #here is the function returns string
            else:
                print("You enter the wrong time!\n")
        except:
            print("wrong input format! must be [hh:mm]")        # if anything happens, it forces user to re-input
            return set_time_input()


# main body starts here!
userInput = 0
while userInput != 4:
    print_blanks()
    userInput = int(input("Menu:\n1. Show all activity\n2. Add task\n3. Delete task\n4. Exits Program\n"))

    if userInput == 1:
        # show tasks
        choice = input("do you want to sort the list[Y/N]?")
        show_act(choice)

        input("press enter to continue...")

    elif userInput == 2:
        # add tasks
        prio1 = ""
        while prio1 != "LOW" and prio1 != "MEDIUM" and prio1 != "HIGH":
            prio1 = input("set Priority [Low, Medium, High]:  ").upper()

        time1 = set_time_input()
        des1 = input("Description:\n")

        add_act(prio1, time1, des1)

    elif userInput == 3:
        # delete tasks
        show_act("N")
        try:
            act_index = input("please chose activity to delete by time: ")
        except TypeError:
            print("input must be on table!")
            break

        del_act(act_index)

    elif userInput == 4:
        # exits task
        print("thank you for using the program")

    else:
        print("Please re-enter again")