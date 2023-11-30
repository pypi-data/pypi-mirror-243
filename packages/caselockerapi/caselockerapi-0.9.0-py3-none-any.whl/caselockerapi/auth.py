import base64
import datetime
import json
import os
import requests
import sys
import getpass
import logging

from caselockerapi.utils import format_url

class CaseLockerToken(object):
    TOKEN_AUTH_URL = ""
    TOKEN_REFRESH_URL = ""

    def __init__(self, subdomain,
                 wrapper=None,
                 username=None,
                 password=None):
        self.subdomain = subdomain
        if wrapper:
            self.load_wrapper(wrapper)
        elif username and password:
            self.authenticate(username, password)
        else:
            DOMAIN = os.environ.get('CASELOCKER_DOMAIN')
            USERNAME = os.environ.get('CASELOCKER_USERNAME')
            PASSWORD = os.environ.get('CASELOCKER_PASSWORD')

            if None in [DOMAIN, USERNAME, PASSWORD]:
                logging.info("Please Log In to CaseLocker")

                if DOMAIN == None:
                    DOMAIN = input("[INPT]: CaseLocker Domain: ")
                else:
                    self.InfoMessage("Domain (env): {}".format(DOMAIN))
                if USERNAME == None:
                    USERNAME = input("[INPT]: CaseLocker Username: ")
                else:
                    logging.info("Username (env): {}".format(USERNAME))
                if PASSWORD == None:
                    PASSWORD = getpass.getpass(prompt="[INPT]: CaseLocker Password: ", stream=None)
            self.subdomain = DOMAIN
            self.authenticate(USERNAME, PASSWORD)

    def load_wrapper(self, wrapper):
        self.wrapper = wrapper
        self.token = self.wrapper['token']
        part = self.token.split('.')[1]
        decoded =  base64.b64decode(part + '=' * (len(part) % 4))
        self.parsed_token = json.loads(decoded)
        self.expires = datetime.datetime.fromtimestamp(self.parsed_token['exp'])
        os.environ['cl_su'] = "True" if 'su' in self.wrapper else "False"

    def authenticate(self, username, password):
        self.TOKEN_AUTH_URL = format_url('api-token-auth/')
        self.TOKEN_REFRESH_URL = format_url('api-token-refresh/')
        if os.environ.get('DEBUG'):
            logging.warning("You are working in debug mode; requests made to localhost")
        try:
            token_auth_url = self.TOKEN_AUTH_URL.format(self.subdomain)
            payload = { 'username': username, 'password': password }
            response = requests.post(token_auth_url, json=payload)
            response.raise_for_status()
            self.load_wrapper(response.json())
            #logging.info("Authenticated Successfully as {}@{}".format(username, self.subdomain))
        except requests.exceptions.HTTPError as e:
            logging.error("Failed to Authenticate. Please try again.")
            sys.exit(1)

    def refresh(self):
        token_refresh_url = self.TOKEN_REFRESH_URL.format(self.subdomain)
        payload = { 'token': self.token }
        response = requests.post(token_refresh_url, json=payload)
        response.raise_for_status()
        self.load_wrapper(response.json())

    def __str__(self):
        return self.token
