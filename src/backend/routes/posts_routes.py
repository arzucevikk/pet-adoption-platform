from flask import Blueprint, request, jsonify
import time

from storage import POSTS
from models.post import Post
from services.map_service import get_user_location_from_map_service, haversine_km

posts_bp = Blueprint("posts_bp", __name__)

# Shelter creates an animal post
@posts_bp.route("/", methods=["POST"])
def create_post():
    data = request.get_json(force=True)

    # Required fields (basic validation)
    required = ["shelter_id", "pet_name", "species", "description", "lat", "lon"]
    for r in required:
        if r not in data:
            return jsonify({"error": f"Missing field: {r}"}), 400

    post = Post(
        post_id=int(time.time() * 1000),
        shelter_id=int(data["shelter_id"]),
        pet_name=data["pet_name"],
        species=data["species"],
        description=data["description"],
        lat=float(data["lat"]),
        lon=float(data["lon"]),
        is_active=True
    )

    POSTS.append(post)
    return jsonify({"message": "Post created", "post": post.__dict__}), 201

# View Animal Posts (all active posts)
@posts_bp.route("/", methods=["GET"])
def list_posts():
    active_posts = [p.__dict__ for p in POSTS if p.is_active]
    return jsonify(active_posts), 200

# Use Case: View Nearby Animals
# Steps align: request location -> map service -> filter by distance -> display
@posts_bp.route("/nearby", methods=["GET"])
def nearby_posts():
    # client sends ?lat=...&lon=...&radius_km=5
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    radius_km = float(request.args.get("radius_km", 5))

    if lat is None or lon is None:
        return jsonify({"error": "Location permission/location data required: lat & lon"}), 400

    user_lat, user_lon = get_user_location_from_map_service(lat, lon)

    result = []
    for p in POSTS:
        if not p.is_active:
            continue
        dist = haversine_km(user_lat, user_lon, p.lat, p.lon)
        if dist <= radius_km:
            item = p.__dict__.copy()
            item["distance_km"] = round(dist, 2)
            result.append(item)

    result.sort(key=lambda x: x["distance_km"])
    return jsonify(result), 200