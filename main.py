from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import sqlite3


class MainWidget(BoxLayout):
    def result(self):
        minutes = int(self.minutes.text)
        visits = int(self.visits.text)
        publications = int(self.publications.text)
        films = int(self.films.text)
        conn = sqlite3.connect('app_db.db')
        c = conn.cursor()
        sql = ("INSERT INTO fruits(minutes, visits, publications, films) VALUES(?, ?, ?, ?)")
        data = (minutes, visits, publications, films)
        c.execute(sql, data)
        conn.commit()
        conn.close()
        show_db_results()

def show_db_results():
    con = sqlite3.connect("app_db.db")
    c = con.cursor()
    c.execute("SELECT * FROM fruits")
    records = c.fetchall()
    result = []
    for i in records:
        result.append(i)
    print(result[-1])



class TheLabApp(App):
    def build(self):
        conn = sqlite3.connect('app_db.db')
        c = conn.cursor()
        c.execute("""
                    CREATE TABLE if not exists fruits(
                        minutes integer,
                        visits integer,
                        publications integer,
                        films integer
                    )
                """)
        conn.commit()
        conn.close()

        return MainWidget()


TheLabApp().run()