from __future__ import print_function
from config import app_server, app_headers
import requests

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, card_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': card_text
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Handle Incoming Requests -------------------------------------
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("Full Incoming Event Details: " + str(event))

    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.

    Left commented out for sharing on GitHub, set to actual app id when coping to Lambda
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.c30c2867-91a5-4cc7-8bd3-5148ff1bd18f"):
    #     raise ValueError("Invalid Application ID")

    # Create two main objects from the 'event'
    session = event['session']
    request = event['request']

    # Get or Setup Session Attributes
    # Session Attributes are used to track elements like current question details, last intent/function position, etc
    session_attributes = load_session_attributes(session)
    session["attributes"] = session_attributes

    # Write Session attributes to Lambda log for troubleshooting assistance
    print("Session Attributes: " + str(session["attributes"]))
    # pprint(session["attributes"])

    if session['new']:
        on_session_started({'requestId': request['requestId']}, session)

    if request['type'] == "LaunchRequest":
        return on_launch(request, session)
    elif request['type'] == "IntentRequest":
        return on_intent(request, session)
    elif request['type'] == "SessionEndedRequest":
        return on_session_ended(request, session)

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """
    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response(launch_request, session)

def on_intent(intent_request, session):
    """
    Called when the user specifies an intent for this skill.
    Main logic point to determine what action to take based on users
    request.
    """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    # Get key details from intent_request object to work with easier
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Find the Previous Place if stored
    # "previous_place" is used to deal with intents and responses that are contextual
    try:
        previous_place = session["attributes"]["previous_place"]
    except:
        previous_place = None

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        # User has asked for help, return the help menu
        return get_help(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        # Built-in intent for when user says something like "Stop"
        # Standard End Game Message
        return no_more(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        # Built-in intent for when user says something like "Cancel"
        # Standard End Game Message
        return no_more(intent, session)
    elif intent_name == "StartGame":
        return get_welcome_response(intent, session)
    elif intent_name == "Options":
        return return_options(intent, session)
    elif intent_name == "Results":
        return return_results(intent, session)
    elif intent_name == "Vote":
        return return_vote(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        # For when user provides an answer like "Yes"
        # Depending on the previous question asked, differnet actions must be taken
        if previous_place in ["welcome", "get help"]:
            return return_options(intent, session)
        else:
            # If the a "Yes" response wouldn't make sense based on previous place, end game
            return get_welcome_response(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        # For when user provides an answer like "No"
        # Depending on the previous question asked, differnet actions must be taken
        if previous_place in ["welcom"]:
            return no_more(intent, session)
        else:
            # Default action to end game
            return no_more(intent, session)
    else:
        # If an intent doesn't match anythign above, it is unexpected
        # and raise error.  This is mostly here for development and troubleshooting.
        # Should NOT occur during normal use.
        return get_welcome_response(intent, session)
        # raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] + ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's Intents ------------------
def get_welcome_response(request, session):
    """
    Welcome the user to the application and provide instructions to get started.
    """

    # Setup the response details
    card_title = "Welcome to MyHero."
    text = "Welcome to MyHero.  Let's figure out the best onscreen superhero.  " \
        "Would you like to hear the options?  "
    speech_output = "<speak>" + text + "</speak>"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "<speak>Want to hear the options?  </speak>"
    should_end_session = False

    session["attributes"]["previous_place"] = "welcome"

    return build_response(
        session["attributes"],
        build_speechlet_response(
            card_title,
            speech_output,
            reprompt_text,
            text,
            should_end_session
        )
    )

def return_options(intent, session):
    # Setup the response details
    options = get_options()

    card_title = "MyHero Voting Options."
    text = "The possible hero's you can vote for are as follows.  "
    for option in options:
        text += "%s, " % (option)
    text = text[0:-2] + ".  "
    text += "Who would you like to vote for?  "
    speech_output = "<speak>" + text + "</speak>"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "<speak>Who would you like to vote for?  </speak>"
    should_end_session = False

    session["attributes"]["previous_place"] = "return options"

    return build_response(
        session["attributes"],
        build_speechlet_response(
            card_title,
            speech_output,
            reprompt_text,
            text,
            should_end_session
        )
    )

def return_results(intent, session):
    # Setup the response details
    results = get_results()

    card_title = "MyHero Current Standing."
    text = "The current standings are as follows.  "
    for result in results:
        text += "%s has %s " % (result[0], result[1])
        if int(result[1]) > 1:
            text += "votes.  "
        else:
            text += "vote.  "
    text += "Who would you like to vote for?  "
    speech_output = "<speak>" + text + "</speak>"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "<speak>Who would you like to vote for?  </speak>"
    should_end_session = False

    session["attributes"]["previous_place"] = "return results"

    return build_response(
        session["attributes"],
        build_speechlet_response(
            card_title,
            speech_output,
            reprompt_text,
            text,
            should_end_session
        )
    )

def return_vote(intent, session):
    # Setup the response details
    vote = intent['slots']['superhero']['value']

    entry = check_vote(vote)

    card_title = "MyHero Vote Submitted."
    if entry:
        text = "Thank you for your vote for %s.  It has been recorded.  " % (entry[0])
        speech_output = "<speak>" + text + "</speak>"
        reprompt_text = ""

        # If the user either does not reply to the welcome message or says something
        # that is not understood, they will be prompted again with this text.
        should_end_session = True
    else:
        text = "I couldn't understand your vote.  Please try again.  "
        speech_output = "<speak>" + text + "</speak>"
        reprompt_text = "Please vote again.  "
        should_end_session = False

    session["attributes"]["previous_place"] = "return vote"

    return build_response(
        session["attributes"],
        build_speechlet_response(
            card_title,
            speech_output,
            reprompt_text,
            text,
            should_end_session
        )
    )

def get_help(intent, session):
    '''
    Help function for the skill.
    '''

    card_title = "MyHero Help"
    text = "Looking for help?  MyHero is easy to use.  " \
           "To find out the possible options, just ask 'What are the options?'" \
           "To find out the current standings, just ask 'What are the current standings?" \
           "And to place a vote, just say 'I'd like to vote for MyHero', and say your vote instead of 'MyHero'.  "
    speech_output = "<speak>" \
                    + text + \
                    "<break time=\"500ms\" />" \
                    "Would you like to hear the options?  " \
                    "</speak>"

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "<speak>Well, would you like to hear the options?  </speak>"
    should_end_session = False

    session["attributes"]["previous_place"] = "get help"

    return build_response(
        session["attributes"],
        build_speechlet_response(
            card_title,
            speech_output,
            reprompt_text,
            text,
            should_end_session
        )
    )

def no_more(intent, session):
    '''
    User has indicated they are done.  Provide a message closing the game, and end session.
    '''
    reprompt_text = None
    card_title = "Thanks for your Vote!"

    text = "Thanks so much for stopping by.  It is important we find out who the best hero is.  "
    speech_output = "<speak>" \
                    + text + \
                    "</speak>"
    should_end_session = True

    return build_response(
        session["attributes"],
        build_speechlet_response(
            card_title,
            speech_output,
            reprompt_text,
            text,
            should_end_session
        )
    )

# ---------------- Functions to generate needed information --------------------
# Utilities to interact with the MyHero-App Server
def get_results():
    u = app_server + "/results"
    page = requests.get(u, headers = app_headers)
    tally = page.json()
    tally = sorted(tally.items(), key = lambda (k,v): v, reverse=True)
    return tally

def get_options():
    u = app_server + "/options"
    page = requests.get(u, headers=app_headers)
    options = page.json()["options"]
    return options

def place_vote(vote):
    u = app_server + "/vote/" + vote
    page = requests.post(u, headers=app_headers)
    return page.json()

def check_vote(vote):
    options = get_options()
    lower_options = []
    dash_to_space_options = []
    dash_remove_options = []
    vote_index = False
    for option in options:
        lower_options.append(option.lower())
        dash_to_space_options.append(option.replace("-", " ").lower())
        dash_remove_options.append(option.replace("-", "").lower())

    try:
        vote_index = lower_options.index(vote.lower())
        vote_submit = options[vote_index]
    except ValueError:
        try:
            vote_index = dash_to_space_options.index(vote.lower())
            vote_submit = options[vote_index]
        except ValueError:
            try:
                vote_index = dash_remove_options.index(vote.lower())
                vote_submit = options[vote_index]
            except ValueError:
                print("Couldn't find option for %s.  " % (vote))
                return False

    print("Placing vote for %s.  " % (vote_submit))
    return ((vote_submit, place_vote(vote_submit)))


def load_session_attributes(session):
    '''
    Determine either current, or new session_attributes
    '''
    try:
        # First try to pull from existing session
        session_attributes = session["attributes"]
    except:
        # If fails, this is a new session and create new attributes
        session_attributes = setup_session_attributes()
    return session_attributes

def setup_session_attributes():
    '''
    Sets up initial Math Dog Session Attributes if new session.
    '''
    session_attributes = {}
    return session_attributes


