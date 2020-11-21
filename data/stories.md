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
  - reset_slots

## who acted in
* greet
  - utter_greet
* who_acted_in{"movie_name":null}
  - slot{"movie_name":null}
  - action_who_acted_in
  - reset_slots

## who acted with
* greet
  - utter_greet
* who_acted_with{"actor_name":null}
  - slot{"actor_name":null}
  - action_who_acted_with
  - reset_slots

## directed which movies
* greet
  - utter_greet
* directed_which_movies{"director_name":null}
  - slot{"director_name":null}
  - action_directed_which_movies
  - reset_slots

## acted in which movies
* greet
  - utter_greet
* acted_in_which_movies{"actor_name":null}
  - slot{"actor_name":null}
  - action_acted_in_which_movies
  - reset_slots