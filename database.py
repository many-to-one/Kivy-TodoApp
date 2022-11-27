import sqlite3
from datetime import date


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()

        # create the user and task table if they don't already exist
        #self.create_user_table()
        self.create_task_table()


    def create_task_table(self):
            """Create tasks table"""
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute(""" CREATE TABLE if not exists todo(
                            title text,
                            description text )""")

            conn.commit()
        

    def create_task(self, title, description):
        """Create a task"""
        self.cursor.execute("INSERT INTO todo(title, description) VALUES(?, ?)", (title, description))
        self.conn.commit()

        # GETTING THE LAST ENTERED ITEM SO WE CAN ADD IT TO THE TASK LIST
        self.cursor.execute("SELECT * FROM todo")
        records = self.cursor.fetchall()

        return records

    def get_tasks(self):
        """Get tasks when loggin into the system"""
        #uncomplete_tasks = self.cursor.execute("SELECT id, task, completed FROM tasks WHERE userid=? and completed = 0", (userid,)).fetchall()
        self.cursor.execute("SELECT * FROM todo")
        completed_tasks = self.cursor.fetchall()
        return completed_tasks  #, uncomplete_tasks

    def mark_task_as_complete(self, userid, taskid):
        """Marking tasks as complete"""
        date_completed = date.today()
        self.cursor.execute("UPDATE tasks SET completed=1, date_completed=? WHERE userid=? AND id=?", (date_completed,userid, taskid))
        self.con.commit()

    def mark_task_as_uncomplete(self, userid, taskid):
        """Mark task as uncomplete"""
        self.cursor.execute("UPDATE tasks SET completed=0, date_completed=? WHERE userid=? AND id=?", (None, userid, taskid))
        self.con.commit()

    def delete_task(self, title, description):
        """Delete a task"""
        self.cursor.execute("DELETE FROM todo WHERE title=? AND description=?", (title, description))
        self.conn.commit()

    
    def close_db_connection(self):
        self.conn.close()

    def connect_db(self):
        self.conn = sqlite3.connect('todo.db')