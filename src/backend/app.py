from flask import Flask
from routes.posts_routes import posts_bp
from routes.adoption_routes import adoption_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(posts_bp, url_prefix="/api/posts")
    app.register_blueprint(adoption_bp, url_prefix="/api/adoptions")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)