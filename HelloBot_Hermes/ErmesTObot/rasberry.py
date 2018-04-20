
from main_exception import SafeRequestHandler
import jsonUtil
import logging
from person import Person
from time import sleep

from google.appengine.ext import ndb

PI_COUNTER_ID = "PI_COUNTER"

class Counter(ndb.Model): #ndb.Expando
    value = ndb.IntegerProperty()

def getPiCounterValue():
    c = Counter.get_by_id(PI_COUNTER_ID)
    return c.value

def getPostiOccupati():
    v = getPiCounterValue()
    return "Posti occupati: {} ".format(v)

def setPiCounterValue(value):
    c = Counter.get_by_id(PI_COUNTER_ID)
    c.value = value
    c.put()

def initPiCounter():
    c = Counter(
        id=PI_COUNTER_ID,
        value=0,
    )
    c.put()


class PiPeople(SafeRequestHandler):

    def post(self):
        import key
        import person
        from main import send_message
        body = jsonUtil.json_loads_byteified(self.request.body)
        logging.debug("body: {}".format(body))
        people_count = body['present']
        setPiCounterValue(people_count)
        #katja = person.getPersonById(key.KATJA_T_ID)
        #send_message(katja, "People count: {} ".format(people_count))
        people_in_stats = Person.query(Person.state==5).fetch()
        for p in people_in_stats:
            send_message(p, "Posti occupati: {} ".format(people_count))
            sleep(0.1)