# SHM AIR FREIGHT TELEGRAM BOT

## BOT OBJECTIVES

Bot should be able to do the following:
---------------------------------------

- Register shipments: Users will need to be registered.
    
    Customer Details:
    ---------------
    + Name
    + email
    + phone number

- Notify users of shipment: recieve shipment tracking data and notify users. Track items till it reaches destination (Nigeria) (no registeration needed, tracking is for US shipments only)

    Tracking Details:
    ----------------
    + Tracking number
    + Carrier name
    + Item description

## SOLUTION BREAKDOWN
_As OOP_

- client(dir):
 _Telegram client interface for user. Represents the highest hierarchy of objects_

    - Client
        + Connects telegram API
        + Collects user details (Name, phone number, email)
        + Collect tracking details (tracking number, carrier name, Item description/name)
        + Notify user of shipment order location via email and SMS
    
    - CommandHandlerCallbacks
        + Provides callback functions to process user inputs

- STORE:
   _Object represents self-hosted db or 3rd party db API for storing user details_
   
    - Connects self-hosted db or 3rd party db API
    - Stores user and tracking details gotten from 'Client' object

Tracker:
    - Requests shipment tracking data
    - Provide data to 'CommandHandlerCallbacks' object
