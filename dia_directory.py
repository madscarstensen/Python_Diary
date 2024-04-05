#!/usr/bin/env python3
import sys
import time
import subprocess
import os
import os.path
import json
import textwrap

wrapper = textwrap.TextWrapper(width=80)

SAVE_DIR = "/Users/velo/Code/Diary/Data/"
TMP = SAVE_DIR + "tmp.tmp"
CONF = SAVE_DIR + "config.json"

def clear():
    """Clears the terminal window."""
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


def printer(print_list):
    """Simply prints all elements of a list. These are usually sentences."""
    for elem in print_list:
        print(elem)
    choice = input("\n> ")
    return choice


def new_entry():
    """Creates a new entry."""
    # Create new JSON file with current date
    # Open temporary file in Vim, in which details can be written
    # Copy Vim file contents into JSON
    NAME_DATE = time.strftime("%Y%m%d")
    FILE_NAME = SAVE_DIR + NAME_DATE + ".json"

    if os.path.isfile(FILE_NAME):
        p_list = ["File for today already exists.",
                  "Do you want to (o)verwrite, create (n)ew or (c)ancel?"]
        confirm = printer(p_list)
        clear()

        while confirm not in ("o", "n", "c"):
            print("Invalid choice.")
            confirm = printer(p_list)
            clear()

        if confirm == "n":
            COUNTER = 1
            while (os.path.isfile(FILE_NAME)):
                FILE_NAME = SAVE_DIR + NAME_DATE + "_" + str(COUNTER) + ".json"
                COUNTER += 1
        elif confirm == "c":
            return

    clear()
    write_new_file(FILE_NAME)

    clear()
    save_entry(FILE_NAME)

def write_new_file(file_name):
    """Opens a Vim window and writes the contents to a serialized entry."""
    ACT_DATE = time.strftime("%d/%m/%Y")
    ACT_TIME = time.strftime("%H:%M")

    with open(file_name, "w+") as data:
        MOOD = input("Current mood: ")
        with open(CONF, 'r') as conf:
            CURR_CONF = json.loads(conf.read())
            EDITOR = CURR_CONF["editor"]
            subprocess.run([EDITOR, TMP])

        if os.path.isfile(TMP):
            with open(TMP, "r") as tmp:
                DESC = tmp.read()[:-1]
                data.write('{"time":"' +
                           ACT_TIME +
                           '", "date":"' +
                           ACT_DATE +
                           '", "mood":"' +
                           MOOD +
                           '", "description":"' +
                           DESC +
                           '"}')
            os.remove(TMP)


def save_entry(file_name):
    """Gives a preview after writing a new entry and allows for saving or
    discarding it."""
    with open(file_name, "r") as data:
        if (len(data.read()) > 0):
            data.seek(0)
            CURR_FILE = json.loads(data.read())
            p_list = ["PREVIEW",
                      '{0:5}  {1:10}  {2}\n'.format(CURR_FILE["time"],
                                                    CURR_FILE["date"],
                                                    CURR_FILE["mood"]),
                      wrapper.fill(CURR_FILE["description"]),
                      "\nSave this entry? (y)es or (n)o"]
            confirm = printer(p_list)
            clear()

            while confirm not in ("y", "n", "Y", "N", "yes", "no", "YES", "NO"):
                print("Invalid choice.\n")
                confirm = printer(p_list)
                clear()

            if confirm in ("y", "Y", "yes", "YES"):
                print("Entry saved.\n")
            elif confirm in ("n", "N", "no", "NO"):
                print("Entry deleted.\n")
                os.remove(file_name)

            _ = input("Press ENTER to continue.")
        else:
            os.remove(file_name)


def list_entries():
    """Lists the already written entries."""
    # Read JSON files for dates and present sorted list
    # Choose file to read or edit via numbers like in menu
    DICT, COUNTER = print_entry_list()

    if (COUNTER == 1):
        _ = input("\nNo files. Press ENTER for main menu.")
        return

    p_list = ["\n(r)ead, (d)elete or (e)dit + number.",
              "I.e. 'r2'. Else (c)ancel"]
    choice = printer(p_list)
    clear()

    while (len(choice) < 2 and
           choice[0] not in ("r", "d", "e") or
           (len(choice) >= 2 and int(choice[1:]) >= COUNTER)):
        if choice[0] == "c":
            return
        print("Invalid choice.\n")
        choice = printer(p_list)
        clear()

    with open(DICT[choice[1:]], 'r') as data:
        CURR_FILE = json.loads(data.read())

    p_list = ["PREVIEW",
              '{0:5}  {1:10}  {2}\n'.format(CURR_FILE["time"],
                                            CURR_FILE["date"],
                                            CURR_FILE["mood"]),
              wrapper.fill(CURR_FILE["description"])]

    if choice[0] == 'r':
        p_list.append("\nPress ENTER to continue.")
        printer(p_list)
    elif choice[0] == 'd':
        p_list.append("\nSure you want to delete this entry from " +
                      CURR_FILE["time"] +
                      " " +
                      CURR_FILE["date"] +
                      "?")
        p_list.append("(y)es or (n)o")
        confirm = printer(p_list)
        clear()

        while confirm not in ("y", "n", "Y", "N", "yes", "no", "YES", "NO"):
            print("Invalid choice.\n")
            confirm = printer(p_list)
            clear()

        if confirm in ("y", "Y", "yes", "YES"):
            print("Entry deleted.\n")
            os.remove(DICT[choice[1:]])
            _ = input("Press ENTER to continue.")
    elif choice[0] == 'e':
        p_list.append("\nEdit (m)ood, (d)escription or (c)ancel?")
        confirm = printer(p_list)
        clear()

        while confirm not in ("m", "d", "c"):
            print("Invalid choice.")
            confirm = printer(p_list)
            clear()

        if confirm == "m":
            print("Current mood is: " + CURR_FILE["mood"])
            MOOD = input("Enter new mood: ")
            clear()
            if (confirm_edit(CURR_FILE["time"],
                             CURR_FILE["date"],
                             MOOD,
                             CURR_FILE["description"])):
                with open(DICT[choice[1:]], "w") as data:
                    CURR_FILE["mood"] = MOOD
                    json.dump(CURR_FILE, data)
                    print("File edited and saved.\n")
                    _ = input("Press ENTER to continue.")
        elif confirm == "d":
            with open(TMP, "w") as tmp:
                tmp.write(CURR_FILE["description"])

            with open(CONF, 'r') as conf:
                CURR_CONF = json.loads(conf.read())
                EDITOR = CURR_CONF["editor"]
                subprocess.run([EDITOR, TMP])

            with open(TMP, "r") as tmp:
                DESC = tmp.read()[:-1]
                if (confirm_edit(CURR_FILE["time"],
                                 CURR_FILE["date"],
                                 CURR_FILE["mood"],
                                 DESC)):
                    with open(DICT[choice[1:]], "w") as data:
                        CURR_FILE["description"] = DESC
                        json.dump(CURR_FILE, data)
                        print("File edited and saved.\n")
                        _ = input("Press ENTER to continue.")
            os.remove(TMP)

    clear()
    list_entries()


def print_entry_list():
    """Prints a list of all the available entries."""
    COUNTER = 1
    DICT = {}

    print("Here are the current files:")
    print('{0:6}  {1:5}  {2:10}  {3}'.format("Number", "Time", "Date", "Mood"))
    print('{0:6}  {1:5}  {2:10}  {3}'.format("------", "----", "----", "----"))

    for file in reversed(sorted(os.listdir(SAVE_DIR))):
        if file != "config.json":
            with open(SAVE_DIR + file, 'r') as data:
                data.seek(0)
                CURR_FILE = json.loads(data.read())
                print('{0:6}  {1:5}  {2:10}  {3}'.format(str(COUNTER) + ".",
                                                         CURR_FILE["time"],
                                                         CURR_FILE["date"],
                                                         CURR_FILE["mood"]))
                DICT[str(COUNTER)] = SAVE_DIR + file
                COUNTER += 1
    return (DICT, COUNTER)


def confirm_edit(time, date, mood, desc):
    """Returns a bool reflecting whether an edit to an entry
    should be saved."""
    ret = True
    p_list = ["PREVIEW\n",
              '{0:5}  {1:10}  {2}\n'.format(time,
                                            date,
                                            mood),
              wrapper.fill(desc),
              "\nDo you want to save this new edit?",
              "(y)es or (n)o"]
    confirm = printer(p_list)
    clear()

    while confirm not in ("y", "n", "Y", "N", "yes", "no", "YES", "NO"):
        confirm = printer(p_list)
        clear()

    if confirm in ("n", "N", "no"):
        ret = False

    return ret
