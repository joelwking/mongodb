MongoDB
=========

This role illustrates the use of  module `mongodb_iq` to insert or query documents in a MongoDB.

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

Note: either the variable `mongodb_document` or `mongodb_query` is required, presence of the variable indicates to the program if the intent is to load a document or query a document.

Dependencies
------------

Given this collections is located at `/collections/ansible_collections/joelwking`, the COLLECTIONS_PATHS environment variable will need to be configured or specified in your ansible configuration file.

```bash
export ANSIBLE_COLLECTIONS_PATHS=/collections/
```
Or update your `ansible.cfg` file to include

```
collections_paths = /collections/
```

Example Playbook
----------------

    - name: Load data
      include_role:
        name: mongodb
        tasks_from: insert
      vars:
        # See the role  'defaults/main.yml' for values not specified here
        mongodb_database:  "{{ database }}"
        mongodb_collection: "{{ collection }}"
        mongodb_document: "{{ filename }}"

Refer to the playbook in `tests/test.yml` for an example of loading a document and then issueing a query based on the Object ID returned. There is a sample input file in `files/confections.json` that can be used as input to the test playbook.

```bash
./test.yml -e "filename=/collections/ansible_collections/joelwking/mongodb/roles/mongodb/files/confections.json"

PLAY [load and query MongoDB database] *******************************************************************************

TASK [Gathering Facts] ***********************************************************************************************
ok: [localhost]

TASK [Load data] *****************************************************************************************************

TASK [mongodb : Load JSON file into a MongoDB] ***********************************************************************
changed: [localhost]

TASK [debug] *********************************************************************************************************
ok: [localhost] => {}

MSG:

Document loaded under ObjectID: 5dde8f37e349b508969b6991


TASK [Query data] ****************************************************************************************************

TASK [mongodb : Query document from MongoDB] *************************************************************************
ok: [localhost]

PLAY RECAP ***********************************************************************************************************
localhost                  : ok=4    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

Note, if you executed the `test.yml` playbook with the `-v` option, it will display the *ansible_facts* returned from the program.

License
-------

GPLv3

Author Information
------------------

email: joel.king@wwt.com  GitHub/GitLab: @joelwking 
