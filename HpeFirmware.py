#!/usr/bin/python

import argparse
import sys
import os
import redfish
import json

class HpeFirmware(object):

    def __init__(self, ip_address=None, username=None, password=None):
         self.ip_address = ip_address
         self.username = username
         self.password = password

         self.loadRedfish()
         self.redfishObj.login()

    def __del__(self):
         if self.redfishObj:
              self.redfishObj.logout()

    def loadRedfish(self):
         if not self.ip_address:
            self.ip_address = os.environ['ILO_IP']

         if not self.username:
            self.username = os.environ['ILO_USERNAME']

         if not self.password:
            self.password = os.environ['ILO_PASSWORD']

         login_host = "https://{}".format(self.ip_address)
         self.redfishObj = redfish.redfish_client(base_url=login_host, username=self.username, password=self.password)

    def getIloFirmwares(self):
        firmwareList = []
        firmwareObj = self.redfishObj.get("/redfish/v1/UpdateService/FirmwareInventory")
        for obj in firmwareObj.obj["Members"]:
            firmware = {}
            firmwareResponse = self.redfishObj.get(obj["@odata.id"])
            firmwareDict = firmwareResponse.obj
            firmware['Name'] = firmwareDict['Name']
            firmware['Description'] = firmwareDict['Description']
            firmware['Health'] = None
            firmware['State'] = None
            if firmwareDict.get("Status"):
                firmware['Health'] = firmwareDict["Status"]['Health']
                firmware['State'] = firmwareDict["Status"]['State']
            firmware['Version'] = firmwareDict['Version']
            firmwareList.append(firmware)

        return firmwareList


    def displayFirmwareInfo(self):
        firmwares = self.getIloFirmwares()

        fmt = '{:<40}{:<25}{:<50}'
        print(fmt.format('Description', 'Version', 'Name'))
        for firmware in firmwares:
            print(fmt.format(firmware['Description'], firmware['Version'], firmware['Name']))
            #print(fmt.format(firmware['Name'], firmware['Description'], firmware['Version'], firmware['Health'], firmware['State']))

    def getFirmwareInfo(self):
        firmwares = self.getIloFirmwares()
        print(json.dumps(firmwares))

def exit(code=0):
    sys.exit(code)


################################ PARSING COMMAND LINES ####################################

parser = argparse.ArgumentParser(prog="Hpe Redfish Firmware Utility", description="Utility to gather firmware verions HPE iLO")

exclusiveParser = parser.add_mutually_exclusive_group(required=True)
exclusiveParser.add_argument('-d', "--display", action='store_true', help="Display firmware output")
exclusiveParser.add_argument('-j', "--json", action='store_true', help="Return firmware details as json")

parser.add_argument('-i', "--ip-address", help="IP Address or Hostname of HPE iLO")
parser.add_argument('-u', "--username", help="Username of HPE iLO")
parser.add_argument('-p', "--password", help="Password of HPE iLO")

myargs = parser.parse_args()

redfishObj = HpeFirmware(ip_address=myargs.ip_address, username=myargs.username, password=myargs.password)

if myargs.display:
    redfishObj.displayFirmwareInfo()
elif myargs.json:
    redfishObj.getFirmwareInfo()
