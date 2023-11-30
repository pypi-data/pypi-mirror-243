# Hash controller

Package for file controller via hash creation and storage in a Database.
Actual integration with PostgreSQL, MongoDB and DynamoDB

## Install and Import

Install with pip

    pip install hash_controller

import as:

    from hash_controller.main import HashClient

## Use

The parameters for the functions are:

    customer_uuid: str
    type: str
    obj: dict
    objs: list[dict]

None of them should be empty

To check if an item exist in the database use:

    HashClient.exist(customer_uuid, type, obj)

In order to create a new registry user:

    HashClient.create(customer_uuid, type, obj)

If you want to do the same but as a batch you can use the many functions, using a list of obj

    HashClient.create_many(customer_uuid, type, objs)
    HashClient.exist_many(customer_uuid, type, objs)

Also if you want to get the full items use:

    HashClient.get_many(filter)

with filter as a dict of the data filtered. Example:

    filter = {"customer_uuid": "123"}
    filter = {"created_at": 123456789}
    filter = {"customer_uuid": "123", "type": "user"}
