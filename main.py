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

from Recipe import *
from RecipePage import *
from MainPage import *
from CreateRecipePage import *
from Debug import *
import Settings

# from root.kv

class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if "content" in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)

class AppName(Label):
    pass


class RootWidget(BoxLayout):
    conainer = ObjectProperty(None)


class RecipeApp(App):

    # contains 3 types of pages: Main, recipe and create_recipe
    screen_names = ListProperty(["main", "recipe","create_recipe"])

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
            # switch screen to recipe
            self.root.ids._sm_.switch_to(screen, direction="left")
        else:
            dbg_data = (("{} not found or not valid.\n", recipe_file),
                        ("Looking in: {} .\n", Settings.RECIPE_DIR),
                        ("{}", recipe))
            display_debug(dbg_data)

    #if main screen exist, switch to it
    def loadMainPage(self):

        screen = self.get_screen("main")
        if screen:
            self.root.ids._sm_.switch_to(screen, direction="right")

    def loadCreateRecipePage(self):

        screen = self.get_screen("create_recipe")
        if not screen:
            screen = Builder.load_file(Settings.KV_DIR + "create_recipe.kv")
            self.screens["create_recipe"] = screen

        screen.initPage()

        # switch screen to CreateRecipe page
        self.root.ids._sm_.switch_to(screen, direction="left")

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
