"""All the "main" cardinal functionality should go here."""

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
]


CONNECTION_STR = (
    'mongodb+srv://server:{}@scouting-system-3das1.gcp.mongodb.net/test?retryWrites=true&w=majority'
)
PORT = 27017


CLIENT = None


DB = None


def get_unsent_docs(collection_name: str):
    if collection_name in COLLECTIONS:
        # TODO: get documents from that collection
        # filter through and only return new documents
        return f"Requested data from {collection_name}"

    else:
        return f"The collection '{collection_name}' does not exist. \
To get a list of supported collections, look at /api/supported-collections/"


def get_match_schedule(comp_code: str):
    # TODO: return the actual match schedule
    with open('cardinal/api/hardcoded_test_data/match_schedule.csv') as file:
        return file.read()


def get_teams_list(comp_code: str):
    # TODO: Get the actual teams list
    with open('cardinal/api/hardcoded_test_data/team_list.csv') as file:
        return file.read()
