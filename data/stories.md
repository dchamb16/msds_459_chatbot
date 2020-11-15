## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## ask diet question
* ask_eat_healthy
  - utter_diet_info

## ask stress questions
* ask_lower_stress
 - utter_stress_info

## ask exercise questions
* ask_exercise
  - utter_exercise_info


## interactive_story_1
* greet
    - utter_greet
* ask_eat_healthy
    - utter_diet_info

## survey happy path
* greet
  - utter_greet
* affirm
  - health_form
  - form{"name":"health_form"}
  - form{"name":null}
  - utter_slot_values
* thankyou
  - utter_no_worries
  -utter_goodbye

## survey stop
* greet
  - utter_greet
* affirm
  - health_form
  - form{"name":"health_form"}
* out_of_scope
  - utter_ask_continue
* deny
  - action_deactivate_form
  - form{"name":null}
  - utter_goodbye

## survey continue
* greet
  - utter_greet
* affirm
  - health_form
  - form{"name":"health_form"}
* out_of_scope
  - utter_ask_continue
* affirm
  - health_form
  - form{"name":null}
  - utter_slot_values

## no survey
* greet
  - utter_greet
* deny
  - utter_goodbye

## ask health questions form
* greet 
  - utter_greet
* affirm
  - health_form
  - form{"name":"health_form"}
* ask_exercise
  - utter_exercise_info
  - health_form
  - form{"name":null}
  - utter_goodbye

## who directed
* query_director
  - action_who_directed
  - slot{"movie_name":null}