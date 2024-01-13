#!/usr/bin/python3
"""
review class that inherits from our base class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    # Review model
    # Attributes
    place_id = ''
    user_id = ''
    text = ''
