from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


class CreateRecipeTitle(Label):
    def setText(self, txt):
        print('setting txt: {}'.format(txt))
        self.text = "[b]"+txt+"[/b]"


class CreateRecipeWidget(Screen):

    def setPageTitle(self, txt):
        self.ids['_title_'].setText(txt)


class TextItem(BoxLayout):

    def setDefaultText(self, txt):
        self.ids['_txt_input_'].text = txt


class ListItem(BoxLayout):

    def setDefaultText(self, txt):
        self.ids['_txt_input_'].text = txt
