import kivy

kivy.require('1.9.1') # replace with your current kivy version !

from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

class TitleWidget(Label):

    def setTitle(self, txt):
        print("setting txt: {}".format(txt))
        self.text = "[b]" + txt + "[/b]"

class ScrollableContentTitle(Label):
    pass

class ScrollableContent(BoxLayout):
    pass

class DescriptionWidget(ScrollableContent):

    def setTitle(self, title):
        self.ids["_title_"].text = "[b]" + title + ":\n[/b]"

    def setDescription(self,txt):
        self.ids["_content_"].text = txt

class ListWidget(ScrollableContent):

    def setTitle(self, title):
        self.ids["_title_"].text = "[b]" + title + ":\n[/b]"

    def addItem(self, item):
        print("item: {}".format(item))
        self.ids["_content_"].text += "- " + item + "\n"

    def removeAllItems(self):
        self.ids["_content_"].text = ""

class RecipeWidget(Screen):

    def cleanRecipe(self):
        self.ids._title_.setTitle('')
        self.ids["_description_"].setDescription("")
        self.ids["_ingredients_"].removeAllItems()
        self.ids["_instructions_"].removeAllItems()


    def setRecipe(self, recipe):
        self.cleanRecipe()
        print('setting recipe Screen')
        self.ids._title_.setTitle(recipe.name)
        self.ids["_description_"].setDescription("for " +
                                                 str(recipe.nb_persons) + "persons.")
        self.ids["_ingredients_"].setTitle("Ingredients")
        for item in recipe.ingredients:
            self.ids["_ingredients_"].addItem(item["name"])
        self.ids["_instructions_"].setTitle("Instructions")
        for item in recipe.instructions:
            self.ids["_instructions_"].addItem(item)
