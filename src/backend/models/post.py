class Post:
    def __init__(self, post_id, shelter_id, pet_name, species, description, lat, lon, is_active=True):
        self.id = post_id
        self.shelter_id = shelter_id
        self.pet_name = pet_name
        self.species = species
        self.description = description
        self.lat = lat
        self.lon = lon
        self.is_active = is_active