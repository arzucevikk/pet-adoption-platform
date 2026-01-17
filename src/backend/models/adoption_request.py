class AdoptionRequest:
    def __init__(self, request_id, user_id, post_id, message):
        self.id = request_id
        self.user_id = user_id
        self.post_id = post_id
        self.message = message
        self.status = "Pending"  # Pending / Approved / Rejected