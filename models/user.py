#!/usr/bin/python3
"""
user class that inherits from our base class
"""
from models.base_model import BaseModel
class User(BaseModel):
    # User Model
    # class attributes
    email = ''
    password = ''
    first_name = ''
    last_name = ''
