import yaml
import os

## Recipe class ##

# Contains:
    # - a name
    # - number of personnes
    # - ingredients
    # - instructions

# Is valid if for at least one person and has instructions and ingredients

# Update the ingredients quantities if the nb of persons changes

class Recipe:

    def __init__(self,name_="",nb_=0,ingredients_=[],instructions_=[]):
        self.name = name_
        self.nb_persons = nb_
        self.ingredients = ingredients_
        self.instructions = instructions_

    def changeNbPersons(self,nb):
        self.nb_persons = nb

    def print(self):
        print("Recipe: {} \nfor {} people.".format(self.name,self.nb_persons))

    def isValid(self):
        return (self.name and self.nb_persons>0 and self.ingredients and self.instructions)

    def save(self, filename):
        recipe_header = {
            "name": self.name,
            "nb_persons": self.nb_persons
        }
        recipe_content = {
            "ingredients": {},
            "instructions": self.instructions
        }

        print(recipe_content["instructions"])

        with open(filename, "w") as recipe_file:
            yaml.dump(recipe_header, recipe_file, default_flow_style=False)
            yaml.dump(recipe_content, recipe_file, default_flow_style=False)


## load recipes from a file ##

# Try to load the yaml file and generate the corresponding Recipe object

def loadRecipe(filename):

    try:
        with open(filename) as fr:
            recipe = yaml.load(fr, Loader=yaml.FullLoader)
            print(recipe["name"])
            return Recipe(recipe["name"], recipe["nb_persons"],
                          recipe["ingredients"], recipe["instructions"])
    except (FileNotFoundError, yaml.scanner.ScannerError) as e:
        print(e)
        return Recipe("",0,[],[])
