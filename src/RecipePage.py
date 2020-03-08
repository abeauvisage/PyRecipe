#############################
#    Deprecated Class ?     #
#############################

import kivy

kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import RecipeLoader

# Scrollable area where lists could be displayed and scrolled through
class ScrollableLabel(ScrollView):

	def __init__(self,text=""):
		super(ScrollableLabel,self).__init__()
		self.add_widget(Label(text=text))
		label =	self.children[0]
		label.text_size = self.size
#		self.children[0].size_hint_y = None
#		self.children[0].height = self.children[0].texture_size[1]
		
# Title specific to recipes
class Title(Label):
	def __init__(self,name="Unknown recipe"):
		super(Title,self).__init__()
		self.text = "[b]"+name+"[/b]\n"
		self.markup = True
		self.size_hint = (1,.2)

class ListTitle(Label):
    pass

class ListWidget(ScrollView):
	def __init__(self,name,text_list=[]):
		super(ListWidget,self).__init__()
		label = Label()
#		label.text_size = (label.width,None)
#		label.size_hint_y = None
#		label.height = label.texture_size[1]
		self.add_widget(label)
		self.setList(text_list)
		print("super size {}".format(super(ListWidget,self).size))
		
	def setList(self,text_list):
		print("text size {} ".format(self.size))
		for item in text_list:
			self.children[0].text += ("- "+item+"\n")
		self.children[0].text_size = self.size #(self.children[0].width,None)
#		self.children[0].size_hint_y = None
#		self.children[0].height = self.children[0].texture_size[1]
		

class RecipeWidget(BoxLayout):

    def __init__(self):
        super(RecipeWidget,self).__init__()
        print('Constructing recipe object')
        # text to be displayed for each element of the recipe
        self.description_text = "description:\n"
        self.ingredients_text = "ingredients:\n"
        self.instructions_text = "instructions:\n"

        self.orientation='vertical'
        self.add_widget(Title(current_dir))
        print("title size {}".format(self.children[0].size))
        boxlayout = BoxLayout()
        boxlayout.add_widget(Label(text=self.description_text))
        boxlayout.add_widget(ListWidget(text=self.ingredients_text))
        self.add_widget(boxlayout)
        self.add_widget(ListWidget(text=self.instructions_text))

    def clearRecipe(self):
        self.children[-1].text = ""
        print("clearing Recipe. desc: {}".format(self.description_text))
        self.children[-2].children[1].text=self.description_text;

    def loadRecipe(self,recipe):
        print("Loading Recipe")
        clearRecipe()
        self.children[-1].text = "[b]"+recipe.name+"[/b]"
        self.children[-2].children[1].text += "for {} persons\n".format(recipe.nb_persons)
        for ingredient in recipe.ingredients:
            self.children[-2].children[0].children[0].text += "- "+ingredient["name"]+"\n"
#		for instruction in recipe.instructions:
#			self.children[0].text += ("- "+instruction+"\n")
#		self.children[-2].children[0].setList(recipe.ingredients["name"])
        self.children[0].setList(recipe.instructions)
