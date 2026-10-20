from flask import Flask, request

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    

@app.route("/<resource>", methods=["GET"])
def resource_get(resource):
    pass

@app.route("/<resource>", methods=["POST"])
def resource_post(resource):
    pass

@app.route("/<resource>/<id>", methods=["PATCH"])
def resource_patch(resource, id):
    pass

@app.route("/<resource>/<id>", methods=["DELETE"])
def resource_delete(resource, id):
    pass

if __name__ == "__main__":
    app.run(debug=True)