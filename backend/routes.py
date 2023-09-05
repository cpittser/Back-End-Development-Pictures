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
    if data:
        for img in data:
            if (img["id"] == id):
                return img, 200
        return {"message": "Id not found"}, 404    
    return {"message": "Internal server error"}, 500
        

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["POST"])
def create_picture():
    response = request.json
    if response:
        for img in data:
            if (img["id"] == response["id"]):
                return {"Message": "picture with id "+ str(response["id"]) +" already present"}, 302
        data.append(response)
        return response, 201
    else:
        return {"message": "Internal server error"}, 500

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    response = request.json
    if response:
        for img in data:
            if (img["id"] == id):
                data[data.index(img)] = response
                return {"message": "Success"}, 200
        return {"message": "picture not found"}, 404
    else:
        return {"message": "Internal server error"}, 500

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if (picture["id"] == id):
            data.remove(picture)
            return {"message": "Deleted"}, 204
    return {"message": "picture not found"}, 404

#######################################################################
# ERROR HANDLER
#######################################################################
@app.errorhandler(404)
def api_not_found(error):
    return {"message": "API not found"}, 404
