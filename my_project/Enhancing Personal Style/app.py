# app.py
from flask_wtf import CSRFProtect
from create_app import create_app

app = create_app()
csrf = CSRFProtect(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
