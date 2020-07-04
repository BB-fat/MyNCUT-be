from app import app
from app.utils.DB import DB
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        debug = True
    else:
        debug = False
    DB.connect(debug)
    app.run(host="0.0.0.0", port=8001, debug=True)
