from flask import Flask , render_template , redirect

app = Flask(__name__)

@app.route('/')
def index():
  return  render_template("index.html")


@app.route("/test")
def test():
   return render_template("test.html")

@app.route("/test/eilts")
def eilts():
   return render_template("eilts.html")

if __name__ == '__main__':
    app.run(debug=True)
