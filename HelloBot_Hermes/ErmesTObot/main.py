# -*- coding: utf-8 -*-

import main_fb
import main_telegram

import logging
from time import sleep
import utility
import geoUtils
import key
import person
from person import Person
import date_time_util as dtu
import webapp2
import rasberry

import jsonUtil
STATE_MACHINE = jsonUtil.json_load_byteified(open('state_machine/sm.json'))
STATE_MACHINE_STATES = STATE_MACHINE['states']

import mensa_info


########################
WORK_IN_PROGRESS = False
########################


# ================================
# ================================
# ================================

STATES = {
    0: 'Initial state',
    9: 'Feedback'
}

RESTART_STATE = 0
SETTINGS_STATE = 3
HELP_STATE = 9


# ================================
# BUTTONS
# ================================

BOTTONE_INDIETRO = "🔙 INDIETRO"
BOTTONE_INIZIO = "🏠 TORNA ALL'INIZIO"
BOTTENE_CERCA_MENSA = "🔍🍽 CERCA MENSA"
BOTTONE_FEEDBACK = "📮 FEEDBACK"


BOTTONE_LOCATION = {
    'text': "INVIA POSIZIONE",
    'request_location': True,
}

# ================================
# TEMPLATE API CALLS
# ================================

def send_message(p, msg, kb=None, markdown=True, inline_keyboard=False, one_time_keyboard=False,
         sleepDelay=False, hide_keyboard=False, force_reply=False, disable_web_page_preview=False):
    if p.isTelegramUser():
        return main_telegram.send_message(p, msg, kb, markdown, inline_keyboard, one_time_keyboard,
                           sleepDelay, hide_keyboard, force_reply, disable_web_page_preview)
    else:
        if kb is None:
            kb = p.getLastKeyboard()
        if kb:
            kb_flat = utility.flatten(kb)[:11] # no more than 11
            return main_fb.sendMessageWithQuickReplies(p, msg, kb_flat)
        else:
            return main_fb.sendMessage(p, msg)
        #main_fb.sendMessageWithButtons(p, msg, kb_flat)

def send_photo_png_data(p, file_data, filename):
    if p.isTelegramUser():
        main_telegram.sendPhotoFromPngImage(p.chat_id, file_data, filename)
    else:
        main_fb.sendPhotoData(p, file_data, filename)
        # send message to show kb
        kb = p.getLastKeyboard()
        if kb:
            msg = 'Opzioni disponibili:'
            kb_flat = utility.flatten(kb)[:11] # no more than 11
            main_fb.sendMessageWithQuickReplies(p, msg, kb_flat)

def send_photo_url(p, url, kb=None):
    if p.isTelegramUser():
        main_telegram.sendPhotoViaUrlOrId(p.chat_id, url, kb)
    else:
        #main_fb.sendPhotoUrl(p.chat_id, url)
        import requests
        file_data = requests.get(url).content
        main_fb.sendPhotoData(p, file_data, 'file.png')
        # send message to show kb
        kb = p.getLastKeyboard()
        if kb:
            msg = 'Opzioni disponibili:'
            kb_flat = utility.flatten(kb)[:11]  # no more than 11
            main_fb.sendMessageWithQuickReplies(p, msg, kb_flat)

def sendDocument(p, file_id):
    if p.isTelegramUser():
        main_telegram.sendDocument(p.chat_id, file_id)
    else:
        pass

def sendExcelDocument(p, sheet_tables, filename='file'):
    if p.isTelegramUser():
        main_telegram.sendExcelDocument(p.chat_id, sheet_tables, filename)
    else:
        pass

def sendWaitingAction(p, action_type='typing', sleep_time=None):
    if p.isTelegramUser():
        main_telegram.sendWaitingAction(p.chat_id, action_type, sleep_time)
    else:
        pass


# ================================
# GENERAL FUNCTIONS
# ================================

# ---------
# BROADCAST
# ---------

BROADCAST_COUNT_REPORT = utility.unindent(
    """
    Messaggio inviato a {} persone
    Ricevuto da: {}
    Non rivevuto da : {} (hanno disattivato il bot)
    """
)

#NOTIFICATION_WARNING_MSG = '🔔 Per modificare le notifiche vai su {} → {}.'.format(
#    BOTTONE_IMPOSTAZIONI, BOTTONE_NOTIFICHE)

def broadcast(sender, msg, qry = None, restart_user=False,
              blackList_sender=False, sendNotification=True,
              notificationWarning = False):

    from google.appengine.ext.db import datastore_errors
    from google.appengine.api.urlfetch_errors import InternalTransientError

    if qry is None:
        qry = Person.query()
    qry = qry.order(Person._key) #_MultiQuery with cursors requires __key__ order

    more = True
    cursor = None
    total, enabledCount = 0, 0

    while more:
        users, cursor, more = qry.fetch_page(100, start_cursor=cursor)
        for p in users:
            try:
                #if p.getId() not in key.TESTERS:
                #    continue
                if not p.enabled:
                    continue
                if blackList_sender and sender and p.getId() == sender.getId():
                    continue
                total += 1
                p_msg = msg
                #+ '\n\n' + NOTIFICATION_WARNING_MSG \
                #    if notificationWarning \
                #    else msg
                if send_message(p, p_msg, sleepDelay=True): #p.enabled
                    enabledCount += 1
                    if restart_user:
                        restart(p)
            except datastore_errors.Timeout:
                msg = '❗ datastore_errors. Timeout in broadcast :('
                tell_admin(msg)
                #deferredSafeHandleException(broadcast, sender, msg, qry, restart_user, curs, enabledCount, total, blackList_ids, sendNotification)
                return
            except InternalTransientError:
                msg = 'Internal Transient Error, waiting for 1 min.'
                tell_admin(msg)
                sleep(60)
                continue

    disabled = total - enabledCount
    msg_debug = BROADCAST_COUNT_REPORT.format(total, enabledCount, disabled)
    logging.debug(msg_debug)
    if sendNotification:
        send_message(sender, msg_debug)
    #return total, enabledCount, disabled

def broadcastUserIdList(sender, msg, userIdList, blackList_sender, markdown):
    for id in userIdList:
        p = person.getPersonById(id)
        if not p.enabled:
            continue
        if blackList_sender and sender and p.getId() == sender.getId():
            continue
        send_message(p, msg, markdown=markdown, sleepDelay=True)



# ---------
# Restart All
# ---------

def restartAll(qry = None):
    from google.appengine.ext.db import datastore_errors
    if qry is None:
        qry = Person.query()
    qry = qry.order(Person._key)  # _MultiQuery with cursors requires __key__ order

    more = True
    cursor = None
    total = 0

    while more:
        users, cursor, more = qry.fetch_page(100, start_cursor=cursor)
        try:
            for p in users:
                if p.enabled:
                    if p.state == RESTART_STATE:
                        continue
                    #logging.debug('Restarting {}'.format(p.chat_id))
                    total += 1
                    restart(p)
                sleep(0.1)
        except datastore_errors.Timeout:
            msg = '❗ datastore_errors. Timeout in broadcast :('
            tell_admin(msg)

    logging.debug('Restarted {} users.'.format(total))

# ================================
# UTILIITY TELL FUNCTIONS
# ================================

def tellMaster(msg, markdown=False, one_time_keyboard=False):
    for id in key.ADMIN_IDS:
        p = person.getPersonById(id)
        main_telegram.send_message(
            p, msg, markdown=markdown,
            one_time_keyboard=one_time_keyboard,
            sleepDelay=True
        )

def tellInputNonValidoUsareBottoni(p, kb=None):
    msg = '⛔️ Input non riconosciuto, usa i bottoni qui sotto 🎛'
    send_message(p, msg, kb)

def tellInputNonValido(p, kb=None):
    msg = '⛔️ Input non riconosciuto.'
    send_message(p, msg, kb)

def tell_admin(msg):
    logging.debug(msg)
    for id in key.ADMIN_IDS:
        p = person.getPersonById(id)
        send_message(p, msg, markdown=False)

def send_message_to_person(id, msg, markdown=False):
    p = Person.get_by_id(id)
    send_message(p, msg, markdown=markdown)
    if p and p.enabled:
        return True
    return False

# ================================
# RESTART
# ================================
def restart(p, msg=None):
    if msg:
        send_message(p, msg)
    p.resetTmpVariable()
    redirectToState(p, RESTART_STATE)


# ================================
# SWITCH TO STATE
# ================================
def redirectToState(p, new_state, **kwargs):
    if p.state != new_state:
        logging.debug("In redirectToState. current_state:{0}, new_state: {1}".format(str(p.state), str(new_state)))
        # p.firstCallCategoryPath()
        p.setState(new_state)
    repeatState(p, **kwargs)


# ================================
# REPEAT STATE
# possible arguments: text, location, contact, photo, document, voice
# ================================
def repeatState(p, **kwargs):

    text = kwargs['text'] if 'text' in kwargs.keys() else None
    location = kwargs['location'] if 'location' in kwargs.keys() else None
    contact = kwargs['contact'] if 'contact' in kwargs.keys() else None
    photo = kwargs['photo'] if 'photo' in kwargs.keys() else None
    document = kwargs['document'] if 'document' in kwargs.keys() else None
    voice = kwargs['voice'] if 'voice' in kwargs.keys() else None

    trigger_is_present = text or location or contact or photo or document or voice
    state = str(p.state)
    if state not in STATE_MACHINE_STATES.keys():
        send_message(p, "Something wrong has happened: can't send you to state {}".format(state))
        return
    sm_state = STATE_MACHINE_STATES[state]
    if not trigger_is_present:
        if "instructions" in sm_state:
            kb = sm_state['keyboard'] if 'keyboard' in sm_state else None
            if isinstance(kb, str):
                kb = eval(kb)
            p.setLastKeyboard(kb)
            send_message(p, sm_state["instructions"], kb)
        if "untriggered_actions" in sm_state:
            actions = sm_state['untriggered_actions']
            performActions(p, actions, text)
    else:
        # trigger is present
        kb = p.getLastKeyboard()
        flat_kb = utility.flatten(kb) if kb else None
        valid_triggers = sm_state['triggers']
        if text:
            if 'text' in valid_triggers:
                triggers_text = valid_triggers['text']
                valid_text = [entry['input'] for entry in triggers_text]
                if text in valid_text:
                    index = valid_text.index(text)
                    triggered_entry = triggers_text[index]
                    actions = triggered_entry['actions']
                    performActions(p, actions, text)
                elif '*' in valid_text:
                    logging.debug('In text *')
                    index = valid_text.index('*')
                    triggered_entry = triggers_text[index]
                    if 'validation' in triggered_entry:
                        eval_expression = triggered_entry['validation']
                        eval_expression = eval_expression.replace('__user_input__', text)
                        #logging.debug('eval_expression: {}'.format(eval_expression))
                        eval_pass = eval(eval_expression)
                        if not eval_pass:
                            tellInputNonValidoUsareBottoni(p, kb)
                        else:
                            actions = triggered_entry['actions']
                            performActions(p, actions, text)
                else:
                    tellInputNonValidoUsareBottoni(p, kb)
            else:
                tellInputNonValido(p)
        elif location:
            if 'location' in valid_triggers:
                triggers_location = valid_triggers['location']
                if location:
                    lat, lon = location['latitude'], location['longitude']
                    p.setLocation(lat, lon)
                    img_url, text = mensa_info.getMenseNearPositionImgUrl(lat, lon)
                    # logging.debug('img_url: {}'.format(img_url))
                    if img_url:
                        send_photo_url(p, img_url)
                    send_message(p, text)
                    sendWaitingAction(p)
                    restart(p)
            else:
                tellInputNonValidoUsareBottoni(p, kb)
        else:
            tellInputNonValidoUsareBottoni(p, kb)

#method(p, **kwargs)

FUNCTIONS_LIST = {
    "SEND_TEXT": "action_send_message",
    "SEND_TEXT_ADMIN": "action_send_message_admin",
    "CHANGE_STATE": "action_change_state",
    "SAVE_VAR": "action_save_var",
    "RESTART": "action_restart"
}

def performActions(p, actions, text):
    for action in actions:
        action_type = action['action_type']
        action_params = action['action_params'] if 'action_params' in action else None
        methodName = FUNCTIONS_LIST[action_type]
        method = possibles.get(methodName)
        method(p, action_params, text)


def action_send_message(p, action_params, text):
    msg = action_params['text']
    if 'rasberry' in msg:
        msg = eval(msg)
    elif 'load_var_name' in action_params:
        var_name = action_params['load_var_name']
        var_value = p.getTmpVariable(var_name)
        msg = msg.replace('__loaded_var__', var_value)
        logging.debug('msg before eval: {}'.format(msg))
        msg = eval(msg)
    elif '__user_input__' in msg:
        msg = msg.replace('__user_input__', text)
        msg = eval(msg)
        if msg is None:
            tellInputNonValido(p)
            return
    send_message(p, msg)

def action_send_message_admin(p, action_params, text):
    msg = action_params['text']
    logging.debug('in action_send_message_admin with text={} and msg={}'.format(text, msg))
    if '__user_input__' in msg:
        msg = msg.replace('__user_input__', text)
        msg = eval(msg)
        logging.debug('msg before eval: {}'.format(msg))
        if msg is None:
            tellInputNonValido(p)
            return
    tell_admin(msg)


def action_change_state(p, action_params, text):
    new_state = action_params['new_state']
    redirectToState(p, new_state)

def action_save_var(p, action_params, text):
    var_name = action_params['var_name']
    var_value = text #action_params['var_name']
    p.setTmpVariable(var_name, var_value, put=True)

def action_restart(p, action_params, text):
    restart(p)

# ================================
# UNIVERSAL COMMANDS
# ================================

def dealWithUniversalCommands(p, text):
    from main_exception import deferredSafeHandleException
    if p.isAdmin():
        if text.startswith('/testText '):
            text = text.split(' ', 1)[1]
            if text:
                msg = '🔔 *Messaggio da ErmesTObot* 🔔\n\n' + text
                logging.debug("Test broadcast " + msg)
                send_message(p, msg)
                return True
        if text.startswith('/broadcast '):
            text = text.split(' ', 1)[1]
            if text:
                msg = '🔔 *Messaggio da ErmesTObot* 🔔\n\n' + text
                logging.debug("Starting to broadcast " + msg)
                deferredSafeHandleException(broadcast, p, msg)
                return True
        elif text.startswith('/restartBroadcast '):
            text = text.split(' ', 1)[1]
            if text:
                msg = '🔔 *Messaggio da ErmesTObot* 🔔\n\n' + text
                logging.debug("Starting to broadcast and restart" + msg)
                deferredSafeHandleException(broadcast, p, msg, restart_user=False)
                return True
        elif text.startswith('/textUser '):
            p_id, text = text.split(' ', 2)[1]
            if text:
                p = Person.get_by_id(p_id)
                if send_message(p, text, kb=p.getLastKeyboard()):
                    msg_admin = 'Message sent successfully to {}'.format(p.getFirstNameLastNameUserName())
                    tell_admin(msg_admin)
                else:
                    msg_admin = 'Problems sending message to {}'.format(p.getFirstNameLastNameUserName())
                    tell_admin(msg_admin)
                return True
        elif text.startswith('/restartUser '):
            p_id = text.split(' ')[1]
            p = Person.get_by_id(p_id)
            restart(p)
            msg_admin = 'User restarted: {}'.format(p.getFirstNameLastNameUserName())
            tell_admin(msg_admin)
            return True
        elif text == '/testlist':
            p_id = key.FEDE_FB_ID
            p = Person.get_by_id(p_id)
            main_fb.sendMessageWithList(p, 'Prova lista template', ['one','twp','three','four'])
            return True
        elif text == '/restartAll':
            deferredSafeHandleException(restartAll)
            return True
        elif text == '/restartAllNotInInitialState':
            deferredSafeHandleException(restartAll)
            return True
    return False



## +++++ END OF STATES +++++ ###

def dealWithUserInteraction(chat_id, name, last_name, username, application, text,
                            location, contact, photo, document, voice):

    p = person.getPersonByChatIdAndApplication(chat_id, application)
    name_safe = ' {}'.format(name) if name else ''

    if p is None:
        p = person.addPerson(chat_id, name, last_name, username, application)
        msg = " 😀 Ciao{},\nbenvenuto/a In ErmesTObot!\n".format(name_safe)
        send_message(p, msg)
        restart(p)
        tellMaster("New {} user: {}".format(application, p.getFirstNameLastNameUserName()))
    else:
        # known user
        modified, was_disabled = p.updateUserInfo(name, last_name, username)
        if WORK_IN_PROGRESS and p.getId() not in key.TESTER_IDS:
            send_message(p, "🏗 Il sistema è in aggiornamento, ti preghiamo di riprovare più tardi.")
        elif was_disabled or text in ['/start', 'start', 'START', 'INIZIO']:
            msg = " 😀 Ciao{}!\nBentornato/a in ErmesTObot!".format(name_safe)
            send_message(p, msg)
            restart(p)
        elif text == '/state':
            msg = "You are in state {}: {}".format(p.state, STATES.get(p.state, '(unknown)'))
            send_message(p, msg)
        elif text in ['/settings', 'IMPOSTAZIONI']:
            redirectToState(p, SETTINGS_STATE)
        elif text in ['/help', 'HELP', 'AIUTO']:
            redirectToState(p, HELP_STATE)
        elif text in ['/stop', 'STOP']:
            p.setEnabled(False, put=True)
            msg = "🚫 Hai *disabilitato* ErmesTObot.\n" \
                  "In qualsiasi momento puoi riattivarmi scrivendomi qualcosa."
            send_message(p, msg)
        elif text == '/testapi':
            import requests
            url = 'https://00b501df.ngrok.io/RestfulService_war_exploded/restresources/cafeteria/0/takenSeats'
            r = requests.get(url)
            result = r.json()
            send_message(p, "result: {}".format(result))
        else:
            if not dealWithUniversalCommands(p, text=text):
                logging.debug("Sending {} to state {} with input {}".format(p.getFirstName(), p.state, text))
                repeatState(p, text=text, location=location, contact=contact, photo=photo, document=document,
                            voice=voice)

app = webapp2.WSGIApplication([
    ('/telegram_me', main_telegram.MeHandler),
    ('/telegram_set_webhook', main_telegram.SetWebhookHandler),
    ('/telegram_get_webhook_info', main_telegram.GetWebhookInfo),
    ('/telegram_delete_webhook', main_telegram.DeleteWebhook),
    #(key.FACEBOOK_WEBHOOK_PATH, main_fb.WebhookHandler),
    (key.TELEGRAM_WEBHOOK_PATH, main_telegram.WebhookHandler),
    ('/pi_people', rasberry.PiPeople),
], debug=True)

possibles = globals().copy()
possibles.update(locals())
