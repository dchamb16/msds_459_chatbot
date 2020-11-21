from typing import Any, Text, Dict, List, Union
from dotenv import load_dotenv

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import AllSlotsReset

import requests
import json
import os

from neo_helper import NeoHelper

load_dotenv()

username = 'neo4j'
password = 'password'


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

        return [AllSlotsReset()]

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
        
        return [AllSlotsReset()]

class ActionWhoActedWith(Action):
    def name(self):
        return 'action_who_acted_with'
    
    @staticmethod
    def required_slots(tracker):
        return ['actor_name']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            'actor_name': [
                self.from_entity(entity='actor_name'),
                self.from_intent(intent='deny', value=None),
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

        actor_name = tracker.get_slot('actor_name')

        response = helper.query_acted_with(actor_name)
        if response is not None:
            dispatcher.utter_message(f'{response} acted with {actor_name}')
        else:
            dispatcher.utter_message(f'Sorry, I couln\'t find {actor_name}')

        return [AllSlotsReset()]

class ActionDirectedWhichMovies(Action):

    def name(self):
        return 'action_directed_which_movies'
    
    @staticmethod
    
    def required_slots(tracker):
        return ['director_name']
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            'director_name': [
                self.from_entity(entity='director_name'),
                self.from_intent(intent='deny', value=None),
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
        director_name = tracker.get_slot('director_name')
        response = helper.query_directed(director_name)
    
        if response is not None:
            dispatcher.utter_message(f'{response} was directed by {director_name}')
        else:
            dispatcher.utter_message(f'Sorry, I couldn\'t find {director_name}')
    
        return [AllSlotsReset()]

class ActionActedInWhichMovies(Action):

    def name(self):
        return 'action_acted_in_which_movies'

    @staticmethod
    def required_slots(tracker):
        return ['actor_name']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            'actor_name' : [
                self.from_entity(entity='actor_name'),
                self.from_intent(intent='deny', value=None),
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
        actor_name = tracker.get_slot('actor_name')
        response = helper.query_actor_acted_in(actor_name)

        if response is not None:
            dispatcher.utter_message(f'{actor_name} acted in {response}')
        else:
            dispatcher.utter_message(f'Sorry, I couldn\'t find {actor_name}')

        return [AllSlotsReset()]