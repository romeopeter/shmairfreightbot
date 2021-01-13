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


- Client:
 _Telegram client interface for user. Represents the highest hierarchy of objects_
    + Connects telegram API
    + Client interface for users
    + Collects user details (Name, phone number, email)
    + Collect tracking details (tracking number, carrier name, Item description/name)
    + Requests package tracking data
    + Notifies users via email and SMS

- STORE:
   _Object represents self-hosted db or 3rd party db API for storing user details_
   
    + Connects self-hosted db or 3rd party db API
    + Stores user and tracking details gotten from ROBOT object

- TRACKER:
    _Nothing here yet_
