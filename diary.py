#!/usr/bin/env python3
import json
import sys
import dia_directory

SAVE_DIR = "/Users/velo/Code/Diary/Data/"
CONF = SAVE_DIR + "config.json"


def init():
    """Sets a preferred editor in the config."""
    CURR_CONF = {}
    with open(CONF, "r") as conf:
        CURR_CONF = json.loads(conf.read())

    if CURR_CONF["editor"] == "":
        p_list = ["Please choose your terminal editor of choice:",
                  "1. Vim",
                  "2. Nano"]
        confirm = dia_directory.printer(p_list)
        dia_directory.clear()

        while confirm not in ("1", "2"):
            print("Invalid choice.")
            confirm = dia_directory.printer(p_list)
            dia_directory.clear()

        if confirm == "1":
            CURR_CONF["editor"] = "vim"
        else:
            CURR_CONF["editor"] = "nano"

        with open(CONF, "w") as conf:
            json.dump(CURR_CONF, conf)


def start_point():
    """Menu"""
    dia_directory.clear()
    init()

    p_list = ["Welcome to your personal diary.",
              "What would you like to do?\n",
              "1. New entry",
              "2. List previous entries",
              "3. Exit"]
    confirm = dia_directory.printer(p_list)
    dia_directory.clear()

    while str(confirm) not in ("1", "2", "3"):
        print("Invalid choice.")
        confirm = dia_directory.printer(p_list)
        dia_directory.clear()

    if confirm == "1":
        dia_directory.new_entry()
    elif confirm == "2":
        dia_directory.list_entries()
    else:
        sys.exit()


if __name__ == "__main__":
    while True:
        start_point()
