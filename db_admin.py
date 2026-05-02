import cmd
import os, os.path

import db


class Shell(cmd.Cmd):
    intro = "Welcome to the tikawe-lainaaja database maintenance tool\nFor a list of commands, type '?' or 'help'\n"
    prompt = "(db_admin) "

    def emptyline(self):
        return False

    def do_exit(self, arg):
        "Exits the management tool."
        return True

    def do_init(self, arg):
        "Creates the database file and initializes the database with the schema and categories."
        if os.path.exists(db.DB_PATH):
            print(f"The database file ({db.DB_PATH}) location already exists.")
            return
        print("Initializing...")
        try:
            with open("schema.sql", encoding="utf-8") as f:
                db.execute_script(f.read())
            with open("init.sql", encoding="utf-8") as f:
                db.execute_script(f.read())
        except Exception as e:
            print("Initialization failed with error:", e)
            return
        print("Database initialized!")
    
    def do_wipe(self, arg):
        "Deletes the database file. WILL DESTROY ALL DATA!"
        if not os.path.exists(db.DB_PATH):
            print(f"The database file ({db.DB_PATH}) was not found.")
            return
        path = os.path.abspath(db.DB_PATH)
        answer = input(f"Are you sure you want to DELETE the file {path} (yes/no) ")
        if answer == "yes":
            try:
                os.remove(path)
            except Exception as e:
                print("There was an error while attempting to remove database:", e)
                return
            print("The database file has been removed.")
        else:
            print("Aborting")
            return


if __name__ == "__main__":
    Shell().cmdloop()
