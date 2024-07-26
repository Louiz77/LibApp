from waitress import serve
from app import app, db

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    #serve(app, port='8000')
    app.config['SECRET_KEY'] = 'app'
    app.run(host='0.0.0.0', debug=True)