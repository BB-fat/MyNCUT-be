from flask import Flask
from util.mongoClient import *

class myApp(Flask):
    def __init__(self,name):
        self.DB=mongoClient()
        super().__init__(name)

app=myApp(__name__)

from app import routes