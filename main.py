from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout



class MainWidget(GridLayout):
    pass


class TheLabApp(App):
    def build(self):
        return MainWidget()


TheLabApp().run()