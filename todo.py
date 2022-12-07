from kivy.metrics import dp
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty, \
    BooleanProperty
import sqlite3
from kivy.core.window import Window
import datetime
from datetime import date
from kivymd.uix.behaviors import FakeRectangularElevationBehavior, \
    RectangularElevationBehavior, CommonElevationBehavior
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.snackbar import Snackbar
from database import Database

database = Database()
Window.size = (300, 600)


class TodoCard(CommonElevationBehavior, FloatLayout):
    title = StringProperty()
    description = StringProperty()
    task_checkbox = StringProperty()
    icon_delete = StringProperty()


class TodoApp(MDApp):
    def build(self):
        global sm
        sm = ScreenManager()
        sm.add_widget(Builder.load_file('Todo.kv'))
        sm.add_widget(Builder.load_file('AddTodo.kv'))
        
        return sm

    def on_start(self):
        today = date.today()
        wd = date.weekday(today)
        days = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday'
        ]
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().strftime("%b"))
        day = str(datetime.datetime.now().strftime("%d"))
        sm.get_screen('main').date.text = f"{days[wd]}, {day}, {month}, {year}"
        sql = database.get_tasks()
        for row in sql:
            sm.get_screen('main').todo_list.add_widget(TodoCard(
                title=row[0],
                description=row[1]
            ))

    def on_complete(self, checkbox, value, title, description, bar):
        if value:
            description.text = ''
            bar.md_bg_color = 0, 179/255, 0, 1
            title.text = ''
            bar.md_bg_color = 0, 179/255, 0, 1
        else:
            remove = ['[s]', '[/s]']
            for i in remove:
                description.text = description.text.replace(i, '')
                bar.md_bg_color = 1, 170 / 255, 23 / 255, 1

    def add_todo(self, title, description):
        if title != '' and description != '' and len(title) < 21 and \
                len(description) < 61:
            sql = database.create_task(title, description)

            for row in sql[len(sql)-1:]:
                sm.get_screen('main').todo_list.add_widget(
                    TodoCard(
                        title=row[0],
                        description=row[1]
                    )
                )

            sm.get_screen('add_todo').description.text = ''
            sm.get_screen('add_todo').title.text = ''
            sm.current = 'main'
        elif title == '':
            Snackbar(
                text='The title is missing!',
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.94,
                size_hint_y=.08,
                bg_color=(1, 170/255, 23/255, 1),
                font_size='18sp',
            ).open()
        elif description == '':
            Snackbar(
                text='The description is missing!',
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.94,
                size_hint_y=.08,
                bg_color=(1, 170/255, 23/255, 1),
                font_size='18sp',
            ).open()
        elif len(title) > 21 :
            Snackbar(
                text='The title is to long!',
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.94,
                size_hint_y=.08,
                bg_color=(1, 170/255, 23/255, 1),
                font_size='18sp',
            ).open()
        elif len(description) > 61 :
            Snackbar(
                text='The description is to long!',
                snackbar_x=dp(10),
                snackbar_y=dp(10),
                size_hint_x=.94,
                size_hint_y=.08,
                bg_color=(1, 170/255, 23/255, 1),
                font_size='18sp',
            ).open()

    def delete_current_task(self, value, title, description, bar):
        database.delete_task(title.text, description.text)
        Snackbar(
            text='The task has been deleted!',
            snackbar_x=dp(10),
            snackbar_y=dp(10),
            size_hint_x=.94,
            size_hint_y=.08,
            bg_color=(1, 170 / 255, 23 / 255, 1),
            font_size='18sp',
        ).open()
        if value:
            description.text = f'[s]{description.text}[/s]'
            bar.md_bg_color = 0, 179/255, 0, 1
            title.text = f'[s]{title.text}[/s]'
            bar.md_bg_color = 0, 179/255, 0, 1

TodoApp().run()