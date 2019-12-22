from app import app
import sys
from setting import *

if __name__=="__main__":
    if sys.argv[1]=="-d":
        DEBUG=True
    app.run(host="127.0.0.1",port=8080,debug=DEBUG)