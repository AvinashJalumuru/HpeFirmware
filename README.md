# HpeFirmware

Utility to display the firmware versions of HPE iLO.

This utility uses redfish api to gather the facts of HPE iLO and using python redfish module
The output contains the name of the firmware, its version and description

## Pre-requisites


```# pip3 install redfish```


## Usage

```
Usage: HpeFirmware.py [-h] (-d | -j) [-i IP_ADDRESS]
                                    [-u USERNAME] [-p PASSWORD]
```

Utility to gather firmware verions HPE iLO

```
Optional arguments:
  -h, --help            show this help message and exit
  -d, --display         Display firmware output
  -j, --json            Return firmware details as json
  -i IP_ADDRESS, --ip-address IP_ADDRESS
                        IP Address or Hostname of HPE iLO
  -u USERNAME, --username USERNAME
                        Username of HPE iLO
  -p PASSWORD, --password PASSWORD
                        Password of HPE iLO						
```


`-d` option displays the firmware details in columns

`-j` option displays the output in json format


## Notes

If the ip-address, username or password is not provided, the script tries to fetch these details from environmental variables
'ILO_IP'
'ILO_USERNAME'
'ILO_PASSWORD'


## Contributors

[Avinash Jalumuru](mailto:avinash.jalumuru@hpe.com)
