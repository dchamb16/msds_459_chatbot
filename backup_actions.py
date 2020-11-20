from typing import Any, Text, Dict, List, Union
from dotenv import load_dotenv

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import requests
import json
import os

from neo_helper import NeoHelper

load_dotenv()

airtable_api_key = os.getenv("AIRTABLE_API_KEY")
base_id = os.getenv("BASE_ID")
table_name = os.getenv("TABLE_NAME")
username = 'neo4j'
password = 'password'

def create_health_log(confirm_exercise, exercise, sleep, diet, stress, goal):
    request_url=f"https://api.airtable.com/v0/{base_id}/{table_name}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {airtable_api_key}",
    }  
    data = {
        "fields": {
            "Exercised?": confirm_exercise,
            "Type of exercise": exercise,
            "Amount of sleep": sleep,
            "Stress": stress,
            "Diet": diet,
            "Goal": goal,
        }
    }
    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
    return response
    print(response.status_code)


def get_entity_name(tracker: Tracker, entity_type: Text):
    entity_name = tracker.get_slot(entity_type)
    if entity_name:
        return entity_name

    return None

class ActionWhoActedIn(Action):
    def name(self):
        return 'action_who_acted_in'
    
    @staticmethod
    def required_slots(tracker):
        return ['movie_name']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            'movie_name': [
                self.from_entity(entity='movie_name'),
                self.from_intent(intent='deny', value='None'),
            ]
        }

    def run(
        self,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any], 
    ) -> List[Dict]:

        helper = NeoHelper()
        helper.connect_graph(username, password)

        movie_name = tracker.get_slot('movie_name')

        response = helper.query_who_acted_in(movie_name)
        if response is not None:
            dispatcher.utter_message(f'{response} acted in {movie_name}')

        return []

class ActionWhoDirected(Action):
    def name(self):
        return 'action_who_directed'
       
    @staticmethod
    def required_slots(tracker):
        return ['movie_name']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            'movie_name': [
                self.from_entity(entity='movie_name'),
                self.from_intent(intent='deny', value='None'),
            ],
        }

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any], 
    ) -> List[Dict]:

        helper = NeoHelper()
        helper.connect_graph(username, password)

        movie_name = tracker.get_slot('movie_name')

        response = helper.query_who_directed(movie_name)
        if response is not None:
            dispatcher.utter_message(f'{response} directed {movie_name}')
        
        return []



class HealthForm(FormAction):

    def name(self):
        return "health_form"

    @staticmethod
    def required_slots(tracker):

        if tracker.get_slot('confirm_exercise') == True:
            return ["confirm_exercise", "exercise", "sleep",
             "diet", "stress", "goal"]
        else:
            return ["confirm_exercise", "sleep",
             "diet", "stress", "goal"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "confirm_exercise": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
                self.from_intent(intent="inform", value=True),
            ],
            "sleep": [
                self.from_entity(entity="sleep"),
                self.from_intent(intent="deny", value="None"),
            ],
            "diet": [
                self.from_text(intent="inform"),
                self.from_text(intent="affirm"),
                self.from_text(intent="deny"),
            ],
            "goal": [
                self.from_text(intent="inform"),
            ],
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        confirm_exercise = tracker.get_slot("confirm_exercise")
        exercise = tracker.get_slot("exercise")
        sleep = tracker.get_slot("sleep")
        stress = tracker.get_slot("stress")
        diet = tracker.get_slot("diet")
        goal = tracker.get_slot("goal")

        response = create_health_log(
                confirm_exercise=confirm_exercise,
                exercise=exercise,
                sleep=sleep,
                stress=stress,
                diet=diet,
                goal=goal
            )

        dispatcher.utter_message("Thanks, your answers have been recorded!")
        return []

