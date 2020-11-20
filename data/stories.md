## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## no survey
* greet
  - utter_greet
* deny
  - utter_goodbye


## who directed
* greet
  - utter_greet
* who_directed{"movie_name":null}
  - slot{"movie_name":null}
  - action_who_directed
  - slot{"movie_name":null}

## who acted in
* greet
  - utter_greet
* who_acted_in{"movie_name":null}
  - slot{"movie_name":null}
  - action_who_acted_in
  - slot{"movie_name":null}

## who acted with
* greet
  - utter_greet
* who_acted_with{"actor_name":null}
  - slot{"actor_name":null}
  - action_who_acted_with
  - slot{"actor_name":null}
