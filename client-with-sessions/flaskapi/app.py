from flask import Flask

app = Flask(__name__)

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