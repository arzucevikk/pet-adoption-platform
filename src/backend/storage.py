# Simple in-memory storage (academic demo)
# You can later replace with SQLite/PostgreSQL easily.

POSTS = []               # animal posts created by shelters
ADOPTION_REQUESTS = []   # adoption requests sent by users

# Basic roles for demo (you can extend)
USERS = [
    {"id": 1, "name": "Alice", "role": "User"},
    {"id": 2, "name": "Happy Shelter", "role": "Shelter"},
    {"id": 3, "name": "Admin", "role": "Administrator"},
]