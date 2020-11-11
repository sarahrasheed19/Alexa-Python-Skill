# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from datetime import datetime
import json
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello! Welcome to the Adelphi Academic Calendar. What can I assist you with?" #after launching skill, Alexa responds with this

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class EventDateIntentHandler(AbstractRequestHandler): #gives a date for a requested event
    """Handler for Event Date Intent. (Sarah)"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("EventDateIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots

        # opens json file
        with open('AdelphiCalendar.json') as json_data:
            data = json.load(json_data)

        # search_date searches through loaded json for corresponding date with the event as a parameter
        def search_date(event):
            for val in data:
                if event.find('1st') != -1:
                    event = event.replace("1st", "first") # alexa takes in "first" as "1st", so this reverts it back to its orignal word
                if event.find('slash') != -1: # alexa takes in "/" as "slash", so this reverts it back to a /
                    event = event.replace('slash', '/')
                    event = re.sub(' ([@.#$\/:-]) ?',r'\1', event) # removes whitespace around /
                if val['event'].lower().find(event.lower()) != -1: # compares inputted event name to all event names in json
                    return val['date'] # returns corresponding date

        try:
            if (search_date(slots["eventName"].value) != None):
                speak_output = "The " + slots["eventName"].value + " is occurring on " + search_date(slots["eventName"].value) # output with returned date
            else:
                speak_output = "The function does not work." # returned this output for testing purposes
        except:
            speak_output = "I could not get that date for you. Try again." # this means alexa was not able to retrieve the event name from user
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to know anything else?")
                .response
        )

class TermIntentHandler(AbstractRequestHandler): #gives a date for a requested event
    """Handler for TermIntent Intent. (Rob)"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TermIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots

        # loads json for searching
        with open('AdelphiCalendar.json') as json_data:
            data = json.load(json_data)

        # search_term searches for the term an event is in
        def search_term(event):
            for val in data:
                if event.find('1st') != -1:
                    event = term.replace("1st", "first")
                if event.find('slash') != -1:
                    event = event.replace('slash', '/')
                    event = re.sub(' ([@.#$\/:-]) ?',r'\1', term)
                if val['event'].lower().find(event.lower()) != -1:
                    return val['term']

        try:
            if (search_term(slots["event"].value) != None):
                speak_output = "The " + slots["event"].value + " is occurring in " + search_term(slots["event"].value)
            else:
                speak_output = "The function does not work."
        except:
            speak_output = "I could not get that date for you. Try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to know anything else?")
                .response
        )


class EventNameIntentHandler(AbstractRequestHandler): #gives a name for a requested Date
    """Handler for Event Name Intent. (Steve)"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("EventNameIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots

        # loads json for searching
        with open('AdelphiCalendar.json') as json_data:
            data = json.load(json_data)

        # search_eventName searches through loaded json for corresponding event name with the date as a parameter
        def search_eventName(date):
            datetime_object = datetime.strptime(date, '%Y-%m-%d') # takes Amazon.DATE format and creates a datetime object, for the purposes of extracting month, day, and year
            if (datetime_object.strftime('%Y') == "2021" and datetime_object.month >= 8): # if the year is set to 2021 by alexa and the month is august or later in the year
                datetime_object = datetime_object.replace(year=2020) # set the date back to 2020 for this academic year
            dateString = datetime_object.strftime('%B') + " " + datetime_object.strftime('%d') + ", " + datetime_object.strftime('%Y') # formats the date to match the format in the json file
            for val in data:
                if val['date'].lower().find(dateString.lower()) != -1: # if dateString and date in json match
                    return val['event'] # return corresponding event name

        try:
            if (search_eventName(slots["eventDate"].value) != None):
                speak_output = "The " + search_eventName(slots["eventDate"].value) + " is occuring on " + slots["eventDate"].value
            else:
                speak_output = "No event on that day."
        except:
            speak_output = "I cannot connect to the academic calendar."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Would you like to know anything else?")
                .response
        )



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(EventDateIntentHandler())
sb.add_request_handler(EventNameIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(TermIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
"""References"""
#https://linuxhint.com/search_json_python/
#https://docs.python.org/2/library/datetime.html
#https://docs.python.org/3/library/calendar.html
#https://pypi.org/project/beautifulsoup4/
#https://docs.python.org/3/library/re.html
#https://github.com/alexa/skill-sample-python-first-skill
#https://stackoverflow.com/questions/17043860/how-to-dump-a-dict-to-a-json-file
