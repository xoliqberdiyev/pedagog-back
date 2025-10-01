import firebase_admin
from firebase_admin import credentials, auth

from django.conf import settings

cred = credentials.Certificate(f"{settings.BASE_DIR}firebase/pedagog-c2608-firebase-adminsdk-fbsvc-ed315d9db0.json")
firebase_app = firebase_admin.initialize_app(cred)