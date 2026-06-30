from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
    # Start the server on host 0.0.0.0 (accessible locally and on network)
    # Using config values for PORT and DEBUG
    print(f"Starting Vehicle Scheduler Backend on port {Config.PORT}...")
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)
