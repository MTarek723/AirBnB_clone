#!/usr/bin/python3
"""
city class that inherits from our base class
"""
from models.base_model import BaseModel


class City(BaseModel):
    # City Model
    # Atributes
    state_id = ''
    name = ''
