from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
        return data

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET", "DELETE"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == str(id):
            if request.method == "GET":
                return {"id":{id}}
            elif request.method == "DELETE":
                data.remove(picture)
                return f"DELETE: {id}"
        return {"message": "Picture not found"}, 404
        

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["POST"])
def create_picture():
    new_picture = request.json
    if not new_picture:
        return {"message": "Invalid input parameter"}, 422
    # code to validate new_picture ommited
    try:
        data.append(new_picture)
    except NameError:
        return {"message": "data not defined"}, 500
    return {"message": f"picture with id {new_picture['id']}"}, 200

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
