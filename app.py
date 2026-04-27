from app import create_app
from app.config import Config
from dotenv import load_dotenv
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=Config.APP_PORT)
