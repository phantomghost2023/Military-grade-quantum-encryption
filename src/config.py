
import os

class Config:
    DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:@localhost:5432/quantum_encryption')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key') # Change this in production!
