import os
import json
import hashlib, base64
from datetime import datetime
from html.parser import HTMLParser

from zipfile import ZipFile

from src.Settings import WEEKLY_LIST_DIR


def uncheck_item(todo_list: dict, item: str):
    for item_, id_ in zip(todo_list["done"], todo_list.get("doneIds", [0]*len(todo_list["done"]))):
        if item_ == item:
            todo_list["todo"].append(item_)
            todo_list["done"].pop(item_)
            if todo_list.get("todoIds"):
                todo_list["todoIds"].append(id_)
                todo_list["doneIds"].pop(id_)
                todo_list["stats"].append({"action": "uncheck", "time": 0, "itemId": id_})
            return
        
def create_item(todo_list: dict, item: str):
    todo_list["todo"].append(item)
    if todo_list.get("todoIds"):
        d = hashlib.md5(str(todo_list).encode()).digest()
        todo_list["todoIds"].append(base64.b64encode(d)[:6].decode())

        
class WeeklyList:
    
    def __init__(self, name: str):
        self.name_ = name
        
    def save_archive(self):
        print(f"creating {os.path.join(WEEKLY_LIST_DIR, self.name_) + '.sqd'}")
        with ZipFile(os.path.join(WEEKLY_LIST_DIR, self.name_) + ".sqd", 'w') as zip:
            zip.write(os.path.join(WEEKLY_LIST_DIR, self.name_, "metadata.json"), arcname="metadata.json")
            zip.write(os.path.join(WEEKLY_LIST_DIR, self.name_, "index.html"), arcname="index.html")
        
    def save(self, items: list):
            
        time = datetime.now()
        timestamp = round(time.timestamp() * 1e3)
        metadata = {"creation_date": timestamp,"last_modification_date": timestamp,"rating":-1,"color":"none","keywords":[],"todolists":[{"id":"todolist2pr4sf","todo":[],"done":[],"stats":[],"todoIds":[],"doneIds":[]}],"urls":{},"reminders":[]}

        for item in items:
            create_item(metadata["todolists"][0], item)
        
        with open(os.path.join(WEEKLY_LIST_DIR, self.name_, "metadata.json"), "w") as f:
            metadata = json.dump(metadata, f)
        
        self.save_archive()
            
    def update(self, items: list):
        
        metadata = {}
        with open(os.path.join(WEEKLY_LIST_DIR, self.name_, "metadata.json"), "r") as f:
            metadata = json.load(f)
            
            for item in items:
                if item in metadata["todolists"][0]["done"]:
                    uncheck_item(metadata["todolists"][0], item)
                else:
                    if not item in metadata["todolists"][0]["done"]:
                        create_item(metadata["todolists"][0], item)
                    
        if metadata:
            time = datetime.now()
            metadata["last_modification_date"] = round(time.timestamp() * 1e3)
            with open(os.path.join(WEEKLY_LIST_DIR, self.name_, "metadata.json"), "w") as f:
                metadata = json.dump(metadata, f)
        
        self.save_archive()

class WeeklyListParser(HTMLParser):
           
    def parse(self, filename):
        with ZipFile(filename, 'r') as zipfile:
            with zipfile.open('index.html') as f:
                self.feed(f.read().decode())
            with zipfile.open('metadata.json') as f:
                self.metadata_ = json.load(f)
    
    def handle_starttag(self, tag, attrs):
        if tag == "div":
            attrs = dict(attrs)
            if attrs.get("class") == "todo-list":
                self.id_ = attrs["id"]
                return
                
    def get_id(self):
        if not self.id_:
            print("Please parse an html file first.")
        else:
            return self.id_
        
    def get_todo_list(self):
        if not self.metadata_:
            print("Please parse a metadata json file first.")
        else:
            return self.metadata_["todolists"][0]
    
    def get_stats(self):
        if not self.metadata_:
            print("Please parse a metadata json file first.")
        else:
            return self.metadata_.get("stats")