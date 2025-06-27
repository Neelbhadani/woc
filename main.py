from api import create_app
from dotenv import load_dotenv
import os

load_dotenv()  # Optional, if using a .env locally

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Required for Railway
    app.run(host="0.0.0.0", port=port, debug=True)
