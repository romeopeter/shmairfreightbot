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


ROBOT:
--
 _Telegram client interface for user. Represent the highest hierarchy of objects_
    - Client interface for users
    - Collects user details (Name, phone number, email)
    - Collect tracking details (tracking number, carrier name, Item description/name)
    - Notifies users via email and SMS

STORE:
--
    _Object represents Airtable API for storing user details_
    - Connects Airtable API
    - Stores user and trackinf details gotten from ROBOT object
