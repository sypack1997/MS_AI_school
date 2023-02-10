from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") # http://127.0.0.1:5000
def index():
    return render_template("index.html")

# @app.route("/home") # http://127.0.0.1:5000/home
# def home():
#     return "Hello World!"'''
#     <h1>제목</h1>
#     <p>본문</p>
#     <a href = "~~~">홈페이지 바로가기</a>
#     '''

# @app.route("/user/<user_name>/<int:user_id>") # http://127.0.0.1:5000/user/sypack/2580 >> Hello, sypack(2580)!
# def user(user_name, user_id):
#     return f"Hello, {user_name}({user_id})!"

if __name__ == "__main__":
    app.run(debug=True)