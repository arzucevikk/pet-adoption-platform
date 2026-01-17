# Pet Adoption Platform (Python Flask)

Actors: User, Shelter, Administrator, External Map Service, Notification Service.

## Implemented Use Cases
- View Animal Posts
- View Nearby Animals (filters posts by distance)
- Send Adoption Request (saved as Pending, notifies Shelter)
- Approve/Reject Request (updates status, notifies User)

## Run
```bash
pip install -r requirements.txt
python src/backend/app.py
