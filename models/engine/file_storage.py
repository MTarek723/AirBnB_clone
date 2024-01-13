#!/usr/bin/python3

"""
This file defines the storage system for
the project.
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from datetime import datetime


class ModelNotFoundError(Exception):
    """Raised when an unknown module is passed"""
    def __init__(self, arg="BaseModel"):
        super().__init__(f"Model with name {arg} is not registered!")


class InstanceNotFoundError(Exception):
    """Raised when an unknown id  is passed"""

    def __init__(self, obj_id="", mod="BaseModel"):
        super().__init__(
                f"Insatnce of {mod} with id {obj_id} does not exist!")


class FileStorage:
    """
    This is  will serve as an Object to storage
    """

    """class private varaibles"""
    __objects = {}
    __file_path = 'file.json'
    ourclasses = (
            "BaseModel",
            "User", "City", "State", "Place",
            "Amenity", "Review"
            )

    def __init__(self):
        """constructor"""
        pass

    def all(self):
        """Return all instances stored inside the database"""
        return FileStorage.__objects

    def new(self, obj):
        """Stores a new Object inside the database"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes objects stored and saves them to json file"""
        dicform = {}
        for key, val in FileStorage.__objects.items():
            dicform[key] = val.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(dicform, f)

    def reload(self):
        """de-serialize persisted objects"""
        savedclasses = {"BaseModel": BaseModel,
                        "User": User,
                        "City": City,
                        "State": State,
                        "Place": Place,
                        "Amenity": Amenity,
                        "Review": Review}
        try:
            with open(FileStorage.__file_path, "r") as f:
                decoded = json.load(f)
                for val in decoded.values():
                    class_name = val["__class__"]
                    myclass = savedclasses[class_name]
                    self.new(myclass(**val))
        except FileNotFoundError:
            pass

    def id_finder(self, model, obj_id):
        """Find and return an elemt of model by its id"""
        F = FileStorage
        if model not in F.ourclasses:
            # Invalid Model Name
            raise ModelNotFoundError(model)
        key = model + "." + obj_id
        if key not in F.__objects:
            # invalid id
            raise InstanceNotFoundError(obj_id, model)
        return F.__objects[key]

    def id_destroyer(self, model, obj_id):
        """dlete the class by its id"""
        F = FileStorage
        if model not in F.ourclasses:
            raise ModelNotFoundError(model)
        key = model + "." + obj_id
        if key not in F.__objects:
            raise InstanceNotFoundError(obj_id, model)
        del F.__objects[key]
        self.save()

    def allfinder(self, model=""):
        """Find all instances of a class"""
        if model and model not in FileStorage.ourclasses:
            raise ModelNotFoundError(model)
        results = []
        for key, val in FileStorage.__objects.items():
            if key.startswith(model):
                results.append(str(val))
        return results

    def updater(self, model, idd, field, value):
        """Updates an instance"""
        F = FileStorage
        if model not in F.ourclasses:
            raise ModelNotFoundError(model)

        key = model + "." + idd
        if key not in F.__objects:
            raise InstanceNotFoundError(idd, model)
        if field in ("id", "updated_at", "created_at"):
            # not allowed to be updated
            return
        inst = F.__objects[key]
        try:
            valtype = type(inst.__dict__[field])
            inst.__dict__[field] = valtype(value)
        except KeyError:
            inst.__dict__[field] = value
        finally:
            inst.updated_at = datetime.now()
            self.save()
