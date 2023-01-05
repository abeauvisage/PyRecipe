import copy
import math
import os
import yaml
from datetime import date

from src.Settings import RECIPE_DIR

UNITS = {
    "quantity": ["x"],
    "spoon": ["tbs", "tsp"],
    "weight": ["g", "kg", "mg"],
    "volume": ["L", "dL", "cL", "mL"],
}

SCALING_FACTORS = {"k": 1000, "d": 0.1, "c": 0.01, "m": 0.001}

RECIPE_INDEX_FILE = os.path.join(os.getcwd(),RECIPE_DIR, "index.yaml")

def magnitude_order(num):
    if num == 0:
        return 0

    absnum = abs(num)
    order = math.log10(absnum)
    res = math.floor(order)

    return res

## Recipe class ##

# Contains:
# - a name
# - number of persons
# - ingredients
# - instructions

# Is valid if for at least one person and has instructions and ingredients

# Update the ingredients quantities if the nb of persons changes


class Recipe:
    def __init__(self, name_="", nb_=0, ingredients_=[], instructions_=[], id_=None):
        self.name = name_
        self.nb_persons = nb_
        self.requested_nb_persons = nb_
        self.ingredients = copy.deepcopy(ingredients_)
        self.original_ingredients = copy.deepcopy(ingredients_)
        self.instructions = instructions_
        self.id = id_
    
    @staticmethod
    def load(filename, id_=None):
        try:
            with open(os.path.join(os.getcwd(),RECIPE_DIR, filename)) as fr:
                recipe = yaml.load(fr, Loader=yaml.FullLoader)
                return Recipe(
                    recipe["name"],
                    recipe["nb_persons"],
                    recipe["ingredients"],
                    recipe["instructions"],
                    id_
                )
        except (FileNotFoundError, yaml.scanner.ScannerError) as e:
            print(e)
            return Recipe()

    def change_nb_persons(self, nb):
        self.requested_nb_persons = nb
        for original_ingredient, ingredient in zip(self.original_ingredients, self.ingredients):
            for k in ingredient.keys():
                if k in UNITS.keys():
                    ingredient[k] = original_ingredient[k] * self.requested_nb_persons / self.nb_persons
                    if k == "quantity" or k == "spoon":
                        ingredient[k] = math.ceil(ingredient[k])
            

    def __str__(self):
        return f"Recipe: {self.name} \nfor {self.nb_persons} people. {len(self.ingredients)} ingredient(s) and {len(self.instructions)} instruction(s)."

    def is_valid(self):
        return (
            self.name and self.nb_persons > 0 and self.ingredients and self.instructions
        )

    def list_ingredients(self):
        out = ""
        for ingredient in self.ingredients:
            for k in ingredient.keys():
                if k in UNITS.keys():
                    out += f"- {ingredient[k]}{UNITS[k][0]} "
            out += f"{ingredient['name']}"
            if "description" in ingredient.keys():
                out += f"({ingredient['description']})"
            out += "\n"

        return out
    
    def list_instructions(self):
        out = ""
        for idx, instruction in enumerate(self.instructions):
            out += f"{idx+1}. {instruction}\n"
        return out

    def save(self, filename, overwrite=False):
        if os.path.exists(os.path.join(os.getcwd(), RECIPE_DIR, filename)) and not overwrite:
            print("Recipe file already exists. Cannot overwrite.")
            return False
        if self.requested_nb_persons != self.nb_persons:
            print("Cannot save the recipe. The number of persons has changed")
            return False
        if not self.is_valid():
            print("Recipe invalid, will not be saved.")
            return False
            
        recipe_header = {"name": self.name, "nb_persons": self.nb_persons}
        recipe_content = {
            "ingredients": self.ingredients,
            "instructions": self.instructions,
        }

        with open(os.path.join(os.getcwd(),RECIPE_DIR, filename), "w") as recipe_file:
            yaml.dump(recipe_header, recipe_file, default_flow_style=False)
            yaml.dump(recipe_content, recipe_file, default_flow_style=False)
            
        update_index(recipe_header["name"], filename, self.id)
        return True
            
    def show(self):
        print(self.name)
        print("Ingredients:")
        print(self.list_ingredients())
        print("Instructions:")
        print(self.list_instructions())
        
    def compute_seasonal_score(self):
        score = 0
        with open(os.path.join(os.getcwd(), "rsrc", "ingredients.yaml"), 'r') as ingf:
            ingredients_ref = yaml.load(ingf, Loader=yaml.FullLoader)
            for ingredient_recipe in self.ingredients:
                general_name = get_general_ingredient_name(ingredient_recipe["name"], ingredients_ref)
                if ingredients_ref[general_name].get("season"):
                    if date.today().month in ingredients_ref[general_name]["season"]:
                        score += 0.75
                    else:
                        score += -1.0
        return score

# Helper functions

def list_recipes():
    with open(RECIPE_INDEX_FILE, "r") as rif:
        return yaml.load(rif, Loader=yaml.FullLoader)["recipes"]
    
def get_full_recipe_index():
    with open(RECIPE_INDEX_FILE, "r") as rif:
        return yaml.load(rif, Loader=yaml.FullLoader)

def clean_index(recipe_index, id):
    for key in recipe_index["recipes"].keys():
        if recipe_index["recipes"][key]["id"] == id:
            recipe_index["recipes"].pop(key)

def update_index(recipe_name, recipe_filename, id):
    recipe_index = get_full_recipe_index()
    print("recipe index", recipe_index, id)
    if id is not None and id < recipe_index["current_counter"]:
        print("cleaning")
        clean_index(recipe_index, id)
        recipe_index["recipes"][recipe_name] = {"id": id, "filename": recipe_filename}
    else:
        print("adding", recipe_name)
        recipe_index["recipes"][recipe_name] = {"id": recipe_index["current_counter"], "filename": recipe_filename}
        recipe_index["current_counter"] += 1
        
    with open(RECIPE_INDEX_FILE, "w") as rif:
        yaml.dump(recipe_index, rif, default_flow_style=False)
        

def update_selection(recipe_name):
    recipe_index = get_full_recipe_index()
    recipe_index["recipes"][recipe_name].update({"selection": date.today()})
    
    with open(RECIPE_INDEX_FILE, "w") as rif:
        yaml.dump(recipe_index, rif, default_flow_style=False)
        
def get_ingredient_unit(ingredient):
    for k, v in ingredient.items():
        if k in UNITS.keys():
            return UNITS[k][0], v
    return (None, None)
    
        
def generate_index():
    # generate an empty index
    index = {"current_counter": 1, "recipes": {}}
    with open(RECIPE_INDEX_FILE, "w") as rif:
        yaml.dump(index, rif, default_flow_style=False)

    # update index with every recipe found in the recipe directory
    for recipe_file in os.listdir(os.path.join(os.getcwd(),RECIPE_DIR)):
        if recipe_file.endswith("yaml") and not recipe_file.startswith("index"):
            recipe = Recipe.load(recipe_file)
            if not recipe.name:
                print(f" Recipe in {recipe_file} does not have a name. Skipping...")
            else:
                update_index(recipe.name, recipe_file, None)
            
            
def format_ingredient_name(ingredient_name):
    ingredient_name = ingredient_name.lower()
    ingredient_name = ingredient_name.replace(" ", "")
    
    if ingredient_name.endswith("ies"):
        ingredient_name = ingredient_name[:-3] + "y"
    if ingredient_name.endswith("es"):
        ingredient_name = ingredient_name[:-2]
    if ingredient_name.endswith("s"):
        ingredient_name = ingredient_name[:-1]
        
    return ingredient_name

def get_general_ingredient_name(name, ingredient_dict):
    for ingredient_name, ingredient_obj in ingredient_dict.items():
        possible_names = [format_ingredient_name(ingredient_name)]
        for ingredient_alt in ingredient_obj.get("alternatives", []):
            possible_names.append(format_ingredient_name(ingredient_alt))
        if format_ingredient_name(name) in possible_names:
            return ingredient_name
    
    raise Exception(f"Ingredient '{name}' not known. Please add it. {possible_names}")