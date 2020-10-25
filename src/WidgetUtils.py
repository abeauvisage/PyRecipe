from kivy.uix.boxlayout import BoxLayout


def get_height(self):
    if self.children:
        height = 0
        if isinstance(self, BoxLayout):
            height = self.padding[0] * 2
            height = height + self.spacing * (len(self.children)-1)
            if self.orientation == 'vertical':
                for item in self.children:
                    height = height + get_height(item)
            else:
                max_height = 0
                for item in self.children:
                    current_height = get_height(item)
                    if current_height > max_height:
                        max_height = current_height
                height = height + max_height
        return height
    else:
        return self.height

def refresh_height(self):

    if isinstance(self, BoxLayout):
        self.height = get_height(self)

    if self.children:
        for item in self.children:
            refresh_height(item)
