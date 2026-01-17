from flask import Blueprint, request, jsonify
import time

from storage import ADOPTION_REQUESTS, POSTS
from models.adoption_request import AdoptionRequest
from services.notification_service import notify_shelter, notify_user

adoption_bp = Blueprint("adoption_bp", __name__)

# Use Case: Send Adoption Request
@adoption_bp.route("/", methods=["POST"])
def create_adoption_request():
    data = request.get_json(force=True)

    required = ["user_id", "post_id", "message"]
    for r in required:
        if r not in data:
            return jsonify({"error": f"Missing field: {r}"}), 400

    # Check post is active
    post = next((p for p in POSTS if p.id == int(data["post_id"])), None)
    if post is None or not post.is_active:
        return jsonify({"error": "Selected post is not active or not found"}), 400

    req_obj = AdoptionRequest(
        request_id=int(time.time() * 1000),
        user_id=int(data["user_id"]),
        post_id=int(data["post_id"]),
        message=data["message"]
    )

    ADOPTION_REQUESTS.append(req_obj)

    # Notify Shelter (doc requirement)
    notify_shelter(post.shelter_id, f"New adoption request for post {post.id} (status: Pending)")
    return jsonify({"message": "Request saved as Pending", "request": req_obj.__dict__}), 201

# Shelter reviews requests (list requests for a shelter)
@adoption_bp.route("/shelter/<int:shelter_id>", methods=["GET"])
def list_requests_for_shelter(shelter_id):
    # find posts owned by shelter
    shelter_posts = {p.id for p in POSTS if p.shelter_id == shelter_id}
    reqs = [r.__dict__ for r in ADOPTION_REQUESTS if r.post_id in shelter_posts]
    return jsonify(reqs), 200

# Use Case: Approve or Reject Request
@adoption_bp.route("/<int:request_id>/decision", methods=["POST"])
def decide_request(request_id):
    data = request.get_json(force=True)
    # required: shelter_id, decision ("Approved" or "Rejected")
    required = ["shelter_id", "decision"]
    for r in required:
        if r not in data:
            return jsonify({"error": f"Missing field: {r}"}), 400

    decision = data["decision"]
    if decision not in ["Approved", "Rejected"]:
        return jsonify({"error": "decision must be Approved or Rejected"}), 400

    req_obj = next((r for r in ADOPTION_REQUESTS if r.id == request_id), None)
    if req_obj is None:
        return jsonify({"error": "Request not found"}), 404

    post = next((p for p in POSTS if p.id == req_obj.post_id), None)
    if post is None:
        return jsonify({"error": "Related post not found"}), 404

    # authorize shelter owns the post
    if post.shelter_id != int(data["shelter_id"]):
        return jsonify({"error": "Shelter not authorized for this request"}), 403

    req_obj.status = decision

    # Notify User (doc requirement)
    notify_user(req_obj.user_id, f"Your adoption request #{req_obj.id} has been {decision}.")
    return jsonify({"message": f"Request {decision}", "request": req_obj.__dict__}), 200