from app import app
from setting import *

if __name__=="__main__":
    app.run(host="127.0.0.1",port=8080,debug=DEBUG)