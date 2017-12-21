#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json


def get_poe_ports(auth):
    """
    Function to get list of poe ports from Aruba OS switch
    :param auth:  AOSSAuth class object returned by pyarubaoss.auth
    :return list of poe ports
    :rtype list
    """
    url_poe = "http://" + auth.ipaddr + "/rest/"+auth.version+"/poe/ports"
    try:
        r = requests.get(url_poe, headers=auth.cookie)
        poe_ports = json.loads(r.text)['port_poe']
        return poe_ports
    except requests.exceptions.RequestException as error:
        return "Error:\n" + str(error) + " get_poe_ports: An Error has occured"

def toggle_poe_port(auth, poeOn, myport):
    """
    Function to enable/disable poe ports on Aruba OS switch
    :param auth:  AOSSAuth class object returned by pyarubaoss.auth
    :param poeOn: Boolean desired state of port True = PoE Enabled
    :param myport: port being modified
    :return port status
    :rtype string
    """
    url = "http://" + auth.ipaddr + "/rest/" + auth.version + "/ports/" + myport + "/poe"
    poeOn = 'true' if poeOn else 'false'
    payload = "{\"is_poe_enabled\": " + poeOn + "}"

    try:
        r = requests.request("PUT", url, data=payload, headers=auth.cookie)
        poe_status = json.loads(r.text)['is_poe_enabled']
        r_status = "enabled" if poe_status else "disabled"
        return "PoE is " + r_status + " on port " + myport
    except requests.exceptions.RequestException as error:
        return "Error:\n" + str(error) + " toggle_poe_ports: An Error has occured"
    
