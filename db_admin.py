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
        "creates the database file and initializes the database with the schema."
        if os.path.exists(db.DB_PATH):
            print(f"The database file ({db.DB_PATH}) location already exists.")
            return
        print("Initializing...")
        try:
            db.init_db()
        except Exception as e:
            print("Initialization failed with error:", e)
        print("Database initialized!")
    
    def do_wipe(self, arg):
        "Deletes the database file. WILL DESTROY ALL DATA!"
        if not os.path.exists(db.DB_PATH):
            print(f"The database file ({db.DB_PATH}) was not found.")
            return
        path = os.path.abspath(db.DB_PATH)
        answer = input(f"Are you sure you want to DELETE the file {path} (yes/no) ")
        if answer == "yes":
            os.remove(path)
            print("The database file has been removed.")
        else:
            print("Aborting")
            return



if __name__ == "__main__":
    Shell().cmdloop()
