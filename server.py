from app import app
from settings import HOST, PORT

if __name__ == '__main__':
    app.run(threaded=True, debug=True)
