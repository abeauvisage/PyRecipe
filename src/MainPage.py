from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
import Settings

import os

class Title(Label):
	def setText(self,txt):
		print('setting txt: {}'.format(txt))
		self.text = "[b]"+txt+"[/b]"

class MainWidget(Screen):
	pass

def createMainPage(app):

    # look for the current dir, its content and recipes in RECIPE_DIR
    f1 = os.popen('pwd')
    f2 = os.popen('ls')
    f3 = os.popen('ls '+Settings.RECIPE_DIR)
    current_dir = f1.read()
    content_dir = f2.read()
    recipe_files = f3.read()

    # load main page
    main_page = Builder.load_file(Settings.KV_DIR+'main.kv')
    # update message with recipe files
    main_page.ids['_message_'].text = "Looking for recipes in \n {}".format(current_dir+"/"+Settings.RECIPE_DIR)

    # add each recipe file to the droplist and bind it so it is selected when
    # released
    droplist = DropDown()
    for rf in recipe_files.split('\n'):
        print(rf)
        if rf.endswith(".yaml") or rf.endswith(".yml"):
            btn = Button(text=rf,size_hint_y=None,height='30dp')
            btn.bind(on_release=lambda btn: droplist.select(btn.text))
            droplist.add_widget(btn)

    main_page.ids['_mainbutton_'].bind(on_release=droplist.open)
    droplist.bind(on_select=app.loadRecipePage)
    #droplist.bind(on_select=lambda instance, x: setattr(main_page.ids['_mainbutton_'], 'text', x))
    return main_page
