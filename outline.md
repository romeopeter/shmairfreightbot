## BOT OBJECTIVES

Bot should be able to do the following:
---------------------------------------

1 Register shipments: Users will need to be registered.
    
    Shipment:
    ----------------
    - Name
    - email
    - phone number
    - Item name
    - Caurrier name
    - Tracking id

2 Regiter shipment detail for tracking
    Tracking Details:
    ----------------
    - Caurrier name
    - shipment tracking id

3 Notify users of shipment: recieve shipment tracking data and notify users. Track (tracking is for US shipments only) items till it reaches destination (Nigeria)

## SOLUTION BREAKDOWN

_Solution is broken down to OOP procedure_

- client(dir):
 _Telegram client interface for user. Represents the highest hierarchy of objects_

    - tClient
        + Connects telegram API [done]
        + Ask user whether to register or track shipment [done].
        + Collects shipment registeration details (Name, phone number, email etc)
            * Sending details to 'Store' object to for database storage
        + Collect tracking details (tracking number, caurrier name)
            * Cross-check data with what's stored in DB
            * Send matched data to 'Tracker' object
        + Notify user of shipment order location via email and SMS
            * Recieve tracking data from 'Tracker object'
    
    - callback
        + Provides callback functions for 'tclient' to process and handle instructions.

- STORE:
   _Object represents self-hosted db or 3rd party db API for storing user details_
   
    - Connects self-hosted db or 3rd party db API
    - Store shipment details from user gotten from 'Client' object

Tracker:
    - Connnect to 3rd party API from recieving tracking data
    - Requests shipment tracking data
    - Provide data to 'CommandHandlerCallbacks' object
