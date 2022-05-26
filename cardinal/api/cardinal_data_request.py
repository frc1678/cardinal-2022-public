"""All the "main" cardinal functionality should go here."""
import json
from typing import List, Dict
from pathlib import Path
from pymongo import MongoClient, database

COLLECTIONS = [
    "obj_pit_collection",
    "subj_pit_collection",
    "calc_obj_tim",
    "calc_obj_team",
    "calc_subj_team",
    "calc_predicted_aim",
    "calc_predicted_team",
    "calc_tba_team",
    "calc_pickability",
    "calc_tba_tim",
    "calc_spr",
    "raw_subj_pit",
    # different names
    "predicted_team",
    "subj_team",
    "obj_tim",
    "tba_team",
    "tba_tim",
    "predicted_aim",
    "pickability",
    "tba_cache",
    "obj_team",
    "subj_aim",
    "raw_obj_pit",
    "unconsolidated_obj_tim",
]


CONNECTION_STR = "mongodb+srv://cardinal-web-server:{}@scouting-system-3das1.gcp.mongodb.net/test?authSource=admin&replicaSet=scouting-system-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true"
PORT = 27017


CLIENT: MongoClient = None
DB: database.Database = None


def serialize_documents(docs) -> List[Dict]:
    """Remove the '_id' from each document"""
    docs = list(docs)
    for doc in docs:
        doc.pop("_id", None)

    return docs


def get_unsent_docs(collection_name: str):
    if collection_name not in COLLECTIONS:
        return f"The collection '{collection_name}' does not exist. \
To get a list of supported collections, look at /api/supported-collections/"

    # TODO - Actually get unsent data, not just all of the data
    # available. This will be called the "Data Delta" feature
    collections = DB.list_collection_names()

    return serialize_documents(DB[collection_name].find())

def create_or_update_notes(team_number: str, notes: str):
    """Create or update a team's notes in the database."""
    notes_collection = DB["strategist-notes"]
    return notes_collection.update_one({"team_number": team_number}, {"$set": {"notes": notes}}, upsert=True).acknowledged

def get_notes(team_number: str):
    """Get a team's notes from the database."""
    notes_collection = DB["strategist-notes"]
    notes = notes_collection.find_one({"team_number": team_number})
    if notes is None:
        return ""
    return notes["notes"]

def get_all_notes():
    """Get all notes from the database"""
    notes_collection = DB["strategist-notes"]
    return serialize_documents(notes_collection.find())

def get_match_schedule(comp_code: str):
    name = "static_viewer_files/{}_match_schedule.json"
    full_name = name.format(comp_code)

    if Path(full_name).exists():
        with open(full_name) as file:
            return json.load(file)
    else:
        return f"Error, no file called {full_name}"


def get_teams_list(comp_code: str):
    name = "static_viewer_files/{}_team_list.json"
    full_name = name.format(comp_code)

    if Path(full_name).exists():
        with open(full_name) as file:
            return json.load(file)
    else:
        return f"Error, no file called {full_name}"
