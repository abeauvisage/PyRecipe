from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window

from Recipe import Recipe
from Debug import display_debug
from WidgetUtils import get_height, refresh_height

# TODO: add description as recipe field and save it
# TODO: init, refresh, height as inhereted class
# TODO: solve text width
# TODO: add check when adding an ingredient or instruction (+ name)
# TODO: set scrollview height based on action bar and title

UNIT = {
    'piece(s)': 'quantity',
    'gram(s)': 'weight',
    'liter(s)': 'volume',
}


def get_root(instance):
    parent = instance.parent
    while not (type(parent) is CreateRecipeWidget):
        parent = parent.parent

    return parent


class CreateRecipeWidget(Screen):

    def setPageTitle(self, txt):
        self.ids['_title_'].text = "[b]"+txt+"[b]"

    def create_recipe(self, instance):

        name = self.ids['_ti_title_'].getText()
        nb_persons = self.ids['_nb_persons_'].nb
        ingredients = []
        for ing_item in self.ids['_li_ingredients_'].children:
            if type(ing_item) is IngredientItem:
                ingredient = {'name': ing_item.ids['_name_'].text}
                if not ing_item.ids['_unit_'].text is 'unitless':
                    ingredient[UNIT[ing_item.ids['_unit_'].text]] = \
                        float(ing_item.ids['_quan_'].text)
                if ing_item.ids['_desc_'].text:
                    ingredient['description'] = ing_item.ids['_desc_'].text
                ingredients.append(ingredient)

        instructions = []
        for inst_item in self.ids['_li_instructions_'].children:
            if type(inst_item) is InstructionItem:
                instructions.append(inst_item.ids['_label_'].text)

        print("creating new recipe: {}".format(name))
        recipe = Recipe(name, nb_persons, ingredients, instructions)
        filename = "recipes/" + name.lower().replace(" ", "_") + ".yaml"
        recipe.save(filename)

    def initPage(self):
        debug_data = []
        self.setPageTitle("Create recipe")
        self.ids['_ti_title_'].setLabel("Recipe title: ")
        self.ids['_ti_desc_'].setLabel("Description: ")
        self.ids['_li_ingredients_'].setDefaultText("Ingredients: ")
        self.ids['_li_ingredients_'].header = IngredientHeader()
        self.ids['_li_ingredients_'].header.refresh()
        self.ids['_li_ingredients_'].init()
        self.ids['_li_instructions_'].setDefaultText("Instructions: ")
        instruction_header = TextItem()
        instruction_header.setLabel("instruction: ")
        self.ids['_li_instructions_'].header = instruction_header
        self.ids['_li_instructions_'].init()
        self.ids['_nb_persons_'].init()


        self.ids['_ti_title_'].height = get_height(self.ids['_ti_title_'])
        self.ids['_ti_desc_'].height = get_height(self.ids['_ti_desc_'])
        self.ids['_nb_persons_'].height = get_height(self.ids['_nb_persons_'])
        self.ids['_create_'].bind(on_press=self.create_recipe)

        self.refresh()

    def refresh(self):
        self.ids['_scrollview_'].height = Window.height - 100
        self.ids['_main_layout_'].height = get_height(self)
        refresh_height(self)

    def saveRecipe(self):

        recipe = Recipe(name, nb, ingredients, instructions)
        recipe.save("recipes/test.yaml")


class UnitDD(DropDown):
    pass


class UnitItem(BoxLayout):

    def getText(self):
        return self.ids['_btn_'].text

    def refresh(self):
       self.dd = UnitDD()
       btn = self.ids['_btn_']
       btn.text = "..."
       btn.bind(on_release=self.dd.open)
       for id_ in self.dd.ids:
           self.dd.ids[id_].bind(on_release=lambda b: self.dd.select(b.text))
       self.dd.bind(on_select=lambda instance, x: setattr(btn, 'text', x))


class IngredientHeader(BoxLayout):

    def refresh(self):
        self.ids['_name_'].refresh("Name:")
        self.ids['_quantity_'].refresh("Quantity:")
        self.ids['_unit_'].refresh()
        self.ids["_description_"].refresh("Description (opt):")

    def clear(self):
        self.ids['_name_'].setDefaultText("")
        self.ids['_quantity_'].setDefaultText("")
        self.ids['_unit_'].ids['_btn_'].text = "..."
        self.ids["_description_"].setDefaultText("")



class TextItem(BoxLayout):

    def setLabel(self, txt):
        self.ids['_label_'].text = txt
        self.ids['_label_'].width = str(8 * len(txt)) +'dp'

    def getText(self):
        return self.ids['_txt_input_'].text

    def setDefaultText(self, txt):
        self.ids['_txt_input_'].text = txt

    def refresh(self, txt):
        self.setLabel(txt)
        self.ids['_label_'].width = str(8 * len(txt)) +'dp'


def remove_item(instance):

    parent_list = instance.parent.parent
    parent_item = instance.parent
    if type(parent_list) is ListItem:
        if (type(parent_item) is InstructionItem) or (type(parent_item) is
                                                      IngredientItem):
            parent_list.remove_widget(parent_item)
        else:
            print("[remove_item] item not recognised")
    else:
        print("[remove_item] instance not a list!")

    parent_list.refresh()


def add_item(instance):

    parent_list = instance.parent.parent
    if type(parent_list) is ListItem:
        head = parent_list.header
        if type(head) is TextItem:
            instruction = InstructionItem()
            instruction.ids['_label_'].text = head.ids['_txt_input_'].text
            instruction.ids['_button_'].bind(on_press=remove_item)
            parent_list.add_widget(instruction)
            head.ids["_txt_input_"].text = ""
        if type(head) is IngredientHeader:
            ingredient_it = IngredientItem()
            ingredient = (head.ids['_name_'].getText(),
                          head.ids['_quantity_'].getText(),
                          head.ids['_unit_'].getText(),
                          head.ids['_description_'].getText())
            ingredient_it.setIngredient(ingredient)
            ingredient_it.ids['_button_'].bind(on_press=remove_item)
            parent_list.add_widget(ingredient_it)
            head.clear()
        if not(type(head) is TextItem or type(head) is IngredientHeader):
            print("[add_item] item not recognised")
    else:
        print("[add_item] instance not a list!")

    parent_list.refresh()


class ListItem(BoxLayout):

    @property
    def header(self):
        return self.children[-2]

    @header.setter
    def header(self, widget):
        widget.id = "_header_"
        self.add_widget(widget)
        self.height = get_height(self)

    def setDefaultText(self, txt):
        self.ids['_label_'].text = txt

    def addItem(self, item):
        self.add_widget(item)

    def refresh(self):
        refresh_height(self)
        self.height = get_height(self)
        refresh_height(get_root(self))

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

    def setIngredient(self, ingredient):
        self.ids['_name_'].text = ingredient[0]
        self.ids['_quan_'].text = ingredient[1]
        self.ids['_unit_'].text = ingredient[2]
        self.ids['_desc_'].text = ingredient[3]

    def refresh(self):
        pass


class InstructionItem(BoxLayout):

    def setInstruction(self, txt):
        self.ids['_label_'].text = txt

    def refresh(self):
        pass
