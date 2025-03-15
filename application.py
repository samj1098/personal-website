from flask import Flask

application = Flask(__name__)

@application.route('/')
def home():
    return "<h1>Welcome to My New AWS Flask Website!</h1>"

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080)

