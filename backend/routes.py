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
    if data:
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    res = make_response()
    if data:
        for picture in data:
            if picture["id"] == id:
                return jsonify(picture), 200
        res.status_code = 404
        return res
    return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    req_pic = request.json
    if data:
        for picture in data:
            if picture["id"] == req_pic["id"]:
                return {
                    "Message": f"picture with id {picture['id']} already present"
                }, 302

        data.append(req_pic)
        return jsonify(req_pic), 201

    return {"message": "Internal server error"}, 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    res = make_response()
    req_pic = request.json
    if data or req_pic:
        for i in range(0, len(data)):
            picture = data[i]
            if picture["id"] == id:
                picture["pic_url"] = req_pic["pic_url"]
                picture["event_country"] = req_pic["event_country"]
                picture["event_state"] = req_pic["event_state"]
                picture["event_city"] = req_pic["event_city"]
                picture["event_date"] = req_pic["event_date"]
                return jsonify(picture), 200

        res.status_code = 404
        return res

    return {"message": "Internal server error"}, 500


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    res = make_response()
    if data:
        for i in range(0, len(data)):
            if data[i]["id"] == id:
                data.pop(i)
                return jsonify(data), 204

        res.status_code = 404
        return res

    return {"message": "Internal server error"}, 500
