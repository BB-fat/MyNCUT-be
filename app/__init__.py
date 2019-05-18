from flask import Flask
from util.mongoClient import *

class myApp(Flask):
    def __init__(self,name,debug):
        self.DB=mongoClient(debug)
        super().__init__(name)

app=myApp(__name__,DEBUG)

from app import routes