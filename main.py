from kivy.app import App
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.uix.button import Button
import sqlite3
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable


Window.size = (300, 600)


class MenuScreen(Screen):
    pass


class SuccessScreen(Screen):
    pass


class DataResult(Screen):

    con = sqlite3.connect("app_db.db")
    c = con.cursor()
    c.execute("SELECT * FROM fruits")
    records = c.fetchall()

    data_tables = MDDataTable(
        size_hint=(0.5, 0.5),
        use_pagination=True,
        check=True,
        column_data=[
            ('minuty', dp(30)),
            ('odwiedziny', dp(30)),
            ('publikacje', dp(30)),
            ('filmy', dp(30))
        ],
        row_data=[
            (
                i[:][0],
                i[:][1],
                i[:][2],
                i[:][3],
            )
            for i in records
        ]
    )

    def get_dt(self):
        sm.get_screen('dt').ids.anch.add_widget(self.data_tables)

    def close_dt(self):
        sm.get_screen('dt').ids.anch.remove_widget(self.data_tables)


class MainWidget(BoxLayout, Screen):
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
        self.show_db_results()

    def show_db_results(self):
        con = sqlite3.connect("app_db.db")
        c = con.cursor()
        c.execute("SELECT * FROM fruits")
        records = c.fetchall()
        return records
        #print(result[-1])



class TheLabApp(MDApp):
    def build(self):
        global sm
        sm = ScreenManager()
        #sm.add_widget(Builder.load_file('TheLab.kv'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(MainWidget(name='main'))
        sm.add_widget(DataResult(name='success'))
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

        return sm



TheLabApp().run()