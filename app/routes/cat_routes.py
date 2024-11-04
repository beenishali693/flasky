from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.cat import Cat

cats_bp = Blueprint("cats_bp", __name__, url_prefix="/cats")

@cats_bp.post("")
def create_cat():
    request_body = request.get_json()
    name = request_body["name"]
    color = request_body["color"]
    personality = request_body["personality"]

    new_cat = Cat(name=name, color=color, personality=personality)
    db.session.add(new_cat)
    db.session.commit()

    response = new_cat.to_dict()
    return response, 201

@cats_bp.get("")
def get_all_cats():
    query = db.select(Cat)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Cat.name.ilike(f"%{name_param}%"))

    color_param = request.args.get("color")
    if color_param:
        query = query.where(Cat.color.ilike(f"%{color_param}%"))

    personality_param = request.args.get("personality")
    if personality_param:
        query = query.where(Cat.personality.ilike(f"%{personality_param}%"))
    
    cats = db.session.scalars(query.order_by(Cat.color))

    cats_response = [cat.to_dict() for cat in cats]
    return cats_response

@cats_bp.get("/count")
def get_count():
    query = db.session.query(Cat.name).count()
    return str(query)

@cats_bp.get("/<cat_id>")
def get_one_cat(cat_id):
    cat = validate_cat(cat_id)

    return cat.to_dict()

@cats_bp.put("/<cat_id>")
def update_cat(cat_id):
    cat = validate_cat(cat_id)
    request_body = request.get_json()

    cat.name = request_body["name"]
    cat.color = request_body["color"]
    cat.personality = request_body["personality"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@cats_bp.delete("/<cat_id>")
def delete_cat(cat_id):
    cat = validate_cat(cat_id)

    db.session.delete(cat)
    db.session.commit()

    return Response(status=204, mimetype="application/json")    
    
def validate_cat(cat_id):
    try:
        cat_id = int(cat_id)
    except:
        abort(make_response({"message":f"Cat id {cat_id} invalid"}, 400))
    
    query = db.select(Cat). where(Cat.id == cat_id)
    cat = db.session.scalar(query)

    if not cat:
        response = {"message": f"Cat {cat_id} not found"}
        abort(make_response(response, 404))
    
    return cat