from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from Recipe import Recipe

class CreateRecipeWidget(Screen):

    def setPageTitle(self, txt):
        self.ids['_title_'].text = "[b]"+txt+"[b]"

    def create_recipe(self, instance):

        name = self.ids['_ti_title_'].ids['_txt_input_'].text
        nb_persons = self.ids['_nb_persons_'].nb
        ingredients = []
        instructions = []

        for instruction in self.ids['_li_instructions_'].children:
            try:
                print(instruction.ids['_label_'].text)
                instructions.append(instruction.ids['_label_'].text)
            except KeyError:
                pass

        print("creating new recipe: {}".format(name))
        recipe = Recipe(name, nb_persons, ingredients, instructions)
        recipe.save("recipes/recipe_test.yaml")



    def initPage(self):
        self.setPageTitle("Create recipe")
        self.ids['_ti_title_'].setDefaultLabel("Recipe title: ")
        self.ids['_ti_desc_'].setDefaultLabel("Description: ")
        self.ids['_li_ingredients_'].setDefaultText("Ingredients: ")
        self.ids['_li_ingredients_'].header = IngredientItem()
        self.ids['_li_instructions_'].setDefaultText("Instructions: ")
        instruction_header = TextItem()
        instruction_header.setDefaultLabel("instruction: ")
        self.ids['_li_instructions_'].header = instruction_header
        self.ids['_li_instructions_'].init()
        self.ids['_nb_persons_'].init()


        self.ids['_ti_title_'].height = self.ids['_ti_title_'].getHeight()
        self.ids['_ti_desc_'].height = self.ids['_ti_desc_'].getHeight()
        self.ids['_nb_persons_'].height = self.ids['_nb_persons_'].getHeight()
        #  self.ids['_li_ingredients_'].height = self.ids['_li_ingredients_'].getHeight()
        #  self.ids['_li_instructions_'].height = self.ids['_li_ingredients_'].getHeight()
        print(self.ids['_nb_persons_'].getHeight())
        print(self.ids['_ti_title_'].getHeight())
        print(self.ids['_ti_desc_'].getHeight())
        print(self.ids['_li_instructions_'].getHeight())
        print(self.getHeight())

        self.ids['_create_'].bind(on_press=self.create_recipe)

    def getHeight(self):
        height = 0
        for item in self.ids['_main_layout_'].children:
            try:
                height = height + item.height
            except TypeError:
                pass

        return height


class TextItem(BoxLayout):

    def setDefaultLabel(self, txt):
        self.ids['_label_'].text = txt

    def setDefaultText(self, txt):
        self.ids['_txt_input_'].text = txt

    def getHeight(self):
        height = self.padding[0] * 2
        max_height = 0
        for item in self.children:
            if item.height > max_height:
                max_height = item.height

        return height + max_height


def remove_item(instance):

    parent_list = instance.parent.parent
    parent_item = instance.parent
    if type(parent_list) is ListItem:
        if type(parent_item) is InstructionItem:
            parent_list.remove_widget(parent_item)
        else:
            print("item not recognised")
    else:
        print("instance not a list!")

    parent_list.height = parent_list.getHeight()

def add_item(instance):

    parent_list = instance.parent.parent
    if type(parent_list) is ListItem:
        head = parent_list.header
        if type(head) is TextItem:
            instruction = InstructionItem()
            instruction.ids['_label_'].text = head.ids['_txt_input_'].text
            instruction.ids['_button_'].bind(on_press=remove_item)
            parent_list.add_widget(instruction)
        else:
            print("item not recognised")
    else:
        print("instance not a list!")

    parent_list.height = parent_list.getHeight()

class ListItem(BoxLayout):

    @property
    def header(self):
        return self.ids['_layout_'].children[0]

    @header.setter
    def header(self, widget):
        self.ids['_layout_'].add_widget(widget)

    def setDefaultText(self, txt):
        self.ids['_label_'].text = txt

    def addItem(self, item):
        self.add_widget(item)

    def getHeight(self):
        height = self.padding[0] * (2*len(self.children)) + self.spacing * (len(self.children)-1)

        for item in self.children:
            try:
                height = height + item.getHeight()
            except TypeError:
                pass
            except AttributeError:
                height = height + item.height

        return height

    def init(self):
        self.ids['_button+_'].bind(on_press=add_item)


class NbPersonsItem(BoxLayout):

    @property
    def nb(self):
        return self._nb

    @nb.setter
    def nb(self, value):
        self.ids['_count_'].text = "[b]"+str(value)+" [/b]"
        self._nb = (int)(value)

    def getHeight(self):
        height = self.padding[0] * 2
        max_height = 0
        for item in self.children:
            if item.height > max_height:
                max_height = item.height

        return height + max_height

    def increase(self, instance):
       instance.parent.nb = instance.parent.nb + 1

    def decrease(self, instance):
        if self.nb > 1:
            self.nb = self.nb - 1

    def init(self):
        self._nb = 4
        self.ids['_button+_'].bind(on_press=self.increase)
        self.ids['_button-_'].bind(on_press=self.decrease)


class IngredientItem(BoxLayout):
    pass


class InstructionItem(BoxLayout):

    def setLabel(self, txt):
        self.ids['_label_'].text = txt

    def getHeight(self):
        height = self.padding[0] * 2
        max_height = 0
        for item in self.children:
            if item.height > max_height:
                max_height = item.height

        return height + max_height
