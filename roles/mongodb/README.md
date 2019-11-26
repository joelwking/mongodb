MongoDB
=========

Uses module `mongodb_iq` to insert or query documents in a MongoDB.

Requirements
------------

This role relies on the module `mongodb_iq`, which must be accessable via the collection `joelwking.mongodb` or separately downloaded and saved in `/usr/share/ansible` and referenced by the *library* variable in `ansible.cfg`. 

Role Variables
--------------

See *defaults/main.yml* for default role variables.

| **Variable Name**           | **Required** | **Default** | **Description**    |
|-----------------------------|--------------|-------------|------------------------------------------------------------------------------------------------------------|
| mongodb_hostname            | no           | localhost   | hostname running the MongoDB instance  |
| mongodb_port                | no           | 27017       | listening port|
| mongodb_username            | no           | root        | uid |
| mongodb_password            | no           | ""          | password |
| mongodb_database            | yes          | "my_database" | name of the database |
| mongodb_collection          | yes          | "my_collection" | name of the collection |
| mongodb_document            | no           | None | JSON object to load |
| mongodb_query               | no           | None | key, value pair used for query |

Dependencies
------------

None

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

GPLv3

Author Information
------------------

email: joel.king@wwt.com  GitHub/GitLab: @joelwking 
