import os
from pathlib import Path
from dotenv import load_dotenv

# Load env variables from the workspace root (one level up from vehicle-scheduler-be)
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key')
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('DEBUG', 'true').lower() == 'true'

    # AffordMed Test Server credentials
    TEST_SERVER_BASE_URL = os.environ.get('TEST_SERVER_BASE_URL', 'http://4.224.186.213/evaluation-service')
    CLIENT_ID = os.environ.get('CLIENT_ID', 'de4fcd70-f43b-4eb3-b222-9c46a3c18af7')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET', 'RzZPrmXvKEtekfTV')
    
    # Registration values (used for authentication requests)
    EMAIL = os.environ.get('EMAIL', 'sreedhar_23ecb40@kgkite.ac.in')
    NAME = os.environ.get('NAME', 'sreedhar r')
    ROLL_NO = os.environ.get('ROLL_NO', '23Ecb40')
    ACCESS_CODE = os.environ.get('ACCESS_CODE', 'WjNyCT')
