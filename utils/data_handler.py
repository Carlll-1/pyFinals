import pickle
import os

DATA_FILE = "hr_data.pkl"

def save_data(data):
    with open(DATA_FILE, "wb") as f:
        pickle.dump(data, f)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "rb") as f:
            return pickle.load(f)
    return {"jobs": [], "applicants": []}