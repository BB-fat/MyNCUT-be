from app import app
from setting import *

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=DEBUG)