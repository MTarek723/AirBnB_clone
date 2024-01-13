#!/usr/bin/python3
"""
this is the base model class for all of our classes here.
"""
from uuid import uuid4
from datetime import datetime
import models

class BaseModel:
    """Base class for all our classes"""
    def __init__(self, *args, **kwargs):
        """initialize  if nothing is passed"""
        if kwargs:
            for key,val in kwargs.items():
                if key == "__class__":
                    pass
                elif key == "created_at" or key == "updated_at":
                    timer = datetime.strptime(val, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, timer)
                else:
                    setattr(self, key, val)
        else:  
            from models import storage
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """overide str representation of self"""
        return "[{}] ({}) {}".format(
                self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """updates the variables"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of class"""
        dicform = {}
        dicform["__class__"] = self.__class__.__name__
        for key, val in self.__dict__.items():
            if isinstance(val, datetime):
                dicform[key] = val.isoformat()
            else:
                dicform[key] = val
        return dicform

    @classmethod
    def all(mycls):
        """Retrieve all current instances of mycls"""
        return models.storage.allfinder(mycls.__name__)

    @classmethod
    def count(mycls):
        """Get the number of all current instances of cls"""
        return len(models.storage.allfinder(mycls.__name__))

    @classmethod
    def create(mycls, *args, **kwargs):
        """Creates an Instance"""
        newcls = mycls(*args, **kwargs)
        return newcls.id

    @classmethod
    def show(mycls, instance_id):
        """Retrieve an instance"""
        return models.storage.id_finder(
            mycls.__name__,
            instance_id
        )

    @classmethod
    def destroy(mycls, instance_id):
        """Deletes an instance"""
        return models.storage.id_destroyer(
            mycls.__name__,
            instance_id
        )

    @classmethod
    def update(mycls, instance_id, *args):
        """Updates an instance
        by the dicform we provide it before"""
        if not len(args):
            print("** attribute name missing **")
            return
        if len(args) == 1 and isinstance(args[0], dict):
            args = args[0].items()
        else:
            args = [args[:2]]
        for arg in args:
            models.storage.updater(
                mycls.__name__,
                instance_id,
                *arg
            )
