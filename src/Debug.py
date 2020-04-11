from kivy.uix.button import Button
from kivy.uix.popup import Popup

def display_debug(debug_data):

	txt = ""
	for data in debug_data:
		txt = txt + data[0].format(data[1]) + "\n"
		
	content = Button(text=txt)
	popup = Popup(title='Debug',content=content, auto_dismiss=False)
	content.bind(on_press=popup.dismiss)

	popup.open()
