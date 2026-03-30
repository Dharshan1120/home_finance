import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-home-finance-key'
    # Use PyMySQL to connect to XAMPP MySQL. By default, user is root and password is "".
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost/home_finance'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-super-secret-key'
    # Set expiration for JWT token to 24 hours
    JWT_ACCESS_TOKEN_EXPIRES = 86400
