import kivy

kivy.require("1.9.1")  # replace with your current kivy version !

import os, sys

sys.path.insert(0, "src/")

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty
from RecipeLoader import *
from MainPage import *
import Settings

# from root.kv
class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if "content" in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)

# List for ingredients, instructions,... or else!
# replace in RecipePage.py
class ListWidget(ScrollView):
    def setTitle(self, title):
        self.text = "[b]" + title + ":\n[/b]"

    def addItem(self, item):
        self.ids["_label_"].text += "- " + item + "\n"

    def removeAllItems(self):
        self.ids["_label_"].text = ""

# replacing RecipePage.py
class RecipeWidget(Screen):

    def cleanRecipe(self):
        self.ids._title_.setText('')
        self.ids["_description_"].text = ""
        self.ids["_ingredients_"].removeAllItems()
        self.ids["_instructions_"].removeAllItems()


    def setRecipe(self, recipe):
        self.cleanRecipe()
        print('setting recipe Screen')
        self.ids._title_.setText(recipe.name)
        self.ids["_description_"].text += "for " + str(recipe.nb_persons) + " persons."
        print(self.ids["_description_"].valign)
        for item in recipe.ingredients:
            self.ids["_ingredients_"].addItem(item["name"])
        for item in recipe.instructions:
            self.ids["_instructions_"].addItem(item)

# Scrollable area to contain lists
class ScrollableLabel(ScrollView):
    def __init__(self, text=""):
        super(ScrollableLabel, self).__init__()
        self.add_widget(Label(text=text))
        label = self.children[0]
        label.text_size = self.size


class Title(Label):
    def setText(self, txt):
        print("setting txt: {}".format(txt))
        self.text = "[b]" + txt + "[/b]"

# from root.kv
class AppName(Label):
    pass


class RootWidget(BoxLayout):
    conainer = ObjectProperty(None)


class RecipeApp(App):

    # contains two types of pages: Main and Recipe
    screen_names = ListProperty(["main", "recipe"])

    def get_screen(self, name):
        if name in self.screens:
            return self.screens[name]
        return False

    def loadRecipePage(self, instance, recipe_file):
        # check if recipe is not already loaded
        screen = self.get_screen("recipe")
        # update the corresponding recipe
        if not screen:
            screen = Builder.load_file(Settings.KV_DIR + "recipe.kv")
            self.screens["recipe"] = screen

        # load recipe
        recipe = loadRecipe(Settings.RECIPE_DIR + "/" + recipe_file)
        if recipe.isValid():
            screen.setRecipe(recipe)
        else:
            screen = Screen()
            screen.add_widget(
                ScrollableLabel(
                    text="Could not find {}\n in {}\n".format(
                        recipe_file, Settings.RECIPE_DIR
                    )
                )
            )
        # switch screen to recipe
        self.root.ids._sm_.switch_to(screen, direction="left")
    

    #if main screen exist, switch to it
    def loadMainPage(self):

        screen = self.get_screen("main")
        if screen:
            self.root.ids._sm_.switch_to(screen, direction="right")

    # load root
    def build(self):

        self.screens = {}
        self.root = Builder.load_file(Settings.KV_DIR + "root.kv")
        screen = createMainPage(self)
        self.screens["main"] = screen
        self.loadMainPage()

        return self.root


if __name__ == "__main__":
    RecipeApp().run()
