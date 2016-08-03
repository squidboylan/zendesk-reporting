What is this?
=============

This is a script that lists Zendesk articles created after the date you specify
in the categories that you specify

Using the script
================

To install dependencies

.. code::

    $ virtualenv venv && . venv/bin/activate && pip install -r requirements.txt

Environment variables to set:
* ZENDESK_URL: Should be set to the domain of your zendesk site
    * Looks something like "https://example.zendesk.com"
* ZENDESK_PASS (OPTIONAL): Should be set to the password of your zendesk user
* EMAIL (OPTIONAL): Should be set to the email of your zendesk user

running the script:

.. code::

    $ python tool.py 2016-01-15 20195786 23965232
