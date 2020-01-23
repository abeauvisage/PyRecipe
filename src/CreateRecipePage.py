from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

class CreateRecipeTitle(Label):
	def setText(self,txt):
		print('setting txt: {}'.format(txt))
		self.text = "[b]"+txt+"[/b]"

class CreateRecipeWidget(Screen):

    def setPageTitle(self,txt):
        self.ids['_title_'].setText(txt)
