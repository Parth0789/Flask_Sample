from app.app import app

@app.before_first_request
def create_table():
    db.create_all()

if __name__ == "__main__":
    from app.db import db
    db.init_app(app)
    app.run(debug=True)