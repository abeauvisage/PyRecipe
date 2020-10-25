from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.metrics import dp

from datetime import date
from calendar import month_name
import yaml

from WidgetUtils import get_height, refresh_height

class SeasonWidget(Screen):

    def load(self):

        filename = "rsrc/fruitsnvegs.yaml";
        try:
            with open(filename) as fr:
                self.list = yaml.load(fr, Loader=yaml.FullLoader)
        except (FileNotFoundError, yaml.scanner.ScannerError) as e:
            display_debug((e, ""))

    def initPage(self):
        self.load()

        this_month = month_name[date.today().month]
        self.change_month(this_month)

        droplist = DropDown()
        for month in month_name[1:]:
            btn = Button(text=month,size_hint_y=None,height='30dp')
            btn.bind(on_release=lambda btn: droplist.select(btn.text))
            droplist.add_widget(btn)

        self.ids['_month_button_'].bind(on_release=droplist.open)
        droplist.bind(on_select=lambda instance, x: self.change_month(x))

        self.refresh();

    def change_month(self, month):
        self.ids["_month_button_"].text = month

        list_fruits = ""
        for fruit in self.list[month]["Fruits"]:
            list_fruits = list_fruits + "- " + fruit +"\n"
        self.ids["_fruits_"].text = list_fruits

        list_veggies = ""
        for veggy in self.list[month]["Vegetables"]:
            list_veggies = list_veggies + "- " + veggy +"\n"
        self.ids["_vegetables_"].text = list_veggies

        self.refresh()

    def refresh(self):
        self.ids['_scrollview_'].height = Window.height - dp(200)
        self.ids['_main_layout_'].height = get_height(self)
        refresh_height(self)
