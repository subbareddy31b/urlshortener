from flask import Flask, render_template, request, redirect, jsonify
import random
import string
import validators

app = Flask(__name__)
dict = {}
@app.route("/")
def home():
    return render_template("index.html")

def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    random_string = ''.join(random.choices(characters, k=length))
    return random_string

@app.route("/sub", methods=["GET", "POST"])
def sub():
    output = None
    method = request.method  # Either "GET" or "POST"
    if method == "POST":
        input_text = request.form.get("inputText")  # Get input from the form
        if not validators.url(input_text):
            output = f"{input_text} is not a valid webiste"    # Process the input
            return render_template("index.html",method=method,output=output)
        random_str = generate_random_string()
        while random_str in dict.keys():
            random_str = generate_random_string()
        shorturl = "http://127.0.0.1:5000/"+ random_str
        dict[random_str] = {"longurl":input_text,"shorturl":shorturl}        
        output = f"{shorturl}"    # Process the input
    return render_template("index.html", method=method, output=output)

@app.route("/<string:single_segment>")
def redirect_to_google(single_segment):
    if single_segment in dict.keys():
        website = dict[single_segment]["longurl"]
        return redirect(website)
    else:
        return render_template("error.html")

@app.route("/<path:any_path>")
def show_error(any_path):
    return render_template("error.html")
if __name__ == "__main__":
    app.run(debug=True)
