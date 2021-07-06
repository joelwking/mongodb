#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': '@joelwking'
}
DOCUMENTATION = '''
---
module: mongodb_iq

short_description: Insert or query a document in a MongoDB database

version_added: "2.9"

description:
    - "Insert or query a document in a MongoDB database."

options:
    database:
        description:
            - Name of the database to query, add or update documents
        required: true
    collection:
        description:
            - Name of the collection in the specified database
        required: true
    document:
        description:
            - The JSON object (dictionary) to load into the collection within the database
        required: false
    query:
        description:
            - A key, value filter (dictionary) used to query the collection within the database
        required: false
    username:
        description:
            - Username used to authenticate with the database
        required: false
        default: root
    password:
        description:
            - Password used to authenticate with the database
        required: false
    authsource:
        description:
            - This database is the authentication database for the user.
        required: false
        default: admin
    host:
        description:
            - hostname or IP address running the database
        required: false
        default: localhost
    port:
        description:
            - port data base is listening on
        required: false
        default: 27017
    protocol:
        description:
            - when connecting to MongoDB Atlas or Digital Ocean managed MongoDB, specify 'mongodb+srv',
            - for a single host running the service, use the default value 'mongodb'
        required: false
        default: mongodb
        choices: ["mongodb", "mongodb+srv"]
    tls:
        description:
            - Use transport layer security (tls), MongoDB Compass refers to this as 'ssl'.
        required: false
        default: false
    tlscafile:
        description:
            - A file containing the download of your cluster’s CA certificate to establish TLS encryption 
            - between the client (this module) and the cluster.
    appname:
        description:
            - The name of the application that created this MongoClient instance. Used for logging.
        required: false
        default: none
    replicaset:
        description:
            - The name of the replica set to connect to.
        required: false
        default: none
    readpreference:
        description:
            - The replica set read preference. One of primary, primaryPreferred, secondary, 
            - secondaryPreferred, or nearest.
        required: false
        default: primary
        choices: ['primary', 'primaryPreferred', 'secondary', 'secondaryPreferred', 'nearest']

author:
    - Joel W. King (@joelwking)
'''

EXAMPLES = '''
---
- name: Gathers facts from a MongoDB database using complex filter
  hosts: localhost

  vars:
    query:
      vzFilter.attributes.name: "MYSQL"

  tasks:
  - name: Run query
    mongodb_iq:
        host: "localhost"
        database:  "ACI"
        collection: "vzFilter"
        query: "{{ query }}"

---
- name: Gathers facts from a MongoDB database, using document _id
  hosts: localhost

  vars:
    query:
      _id: 5a7cc61a1e9c327a3bbef772

  tasks:
  - name: Retrieve data center global variables
    mongo_iq:
        host: "localhost"
        database:  "F5"
        collection: "data_center_global"
        query: "{{ query }}"

---
- name: load a document into a MongoDB database
  hosts: localhost

  - name: load data
    mongodb_iq:
        host: "localhost"
        database:  "ACI"
        collection: "test"
        document: "{{ lookup('file', './library/ansible_hacking.json') }}"

---
 - name: Load JSON file into a Digital Ocean managed MongoDB
    joelwking.mongodb.mongodb_iq:
        host: "{{ inventory_hostname }}"
        username: "{{ mongodb.username }}"
        password: "{{ mongodb.password }}"
        port: "{{ port }}"
        appname: mongodb_iq
        authsource: admin
        protocol: "mongodb+srv"
        readpreference: primary
        replicaset: "db-mongodb-nyc3-59535"
        tls: True
        tlscafile: '{{ playbook_dir }}/files/ca-certificate.crt'
        database:  "{{ database }}"
        collection: "{{ collection }}"
        document: "{{ lookup('file', filename) }}"

  - debug:
        msg: "Document loaded under ObjectID: {{ _id }}"

  - name: Query document from Digital Ocean managed MongoDB
    joelwking.mongodb.mongodb_iq:
        host: "{{ inventory_hostname }}"
        username: "{{ mongodb.username }}"
        password: "{{ mongodb.password }}"
        port: "{{ port }}"
        appname: mongodb_iq
        authsource: admin
        protocol: "mongodb+srv"
        readpreference: primary
        replicaset: "db-mongodb-nyc3-59535"
        tls: True
        tlscafile: '{{ playbook_dir }}/files/ca-certificate.crt'
        database:  "{{ database }}"
        collection: "{{ collection }}"
        query: "{{ query }}"
    vars:
      query:
        _id: '{{ _id }}'
        

'''
# References:
#         http://docs.ansible.com/ansible/latest/common_return_values.html
#         http://altons.github.io/python/2013/01/21/gentle-introduction-to-mongodb-using-pymongo/
#         http://api.mongodb.com/python/current/tutorial.html
#         https://gist.github.com/DavidWittman/10688924
#         https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html
# Issues:
#         Assignment statements in Python do not copy objects, without issuing a
#         copy.deepcopy, when we convert _id to an object for the query, the original value
#         is also converted, upon exiting when running in Ansible, you will see the exception
#         TypeError: Value of unknown type: <class 'bson.objectid.ObjectId'>
#         as the original string value of _id has been replaced with the object format to issue the
#         query.
#
# system imports
#
import urllib
import copy
#
# SDK imports:
#
try:
    import pymongo                      # from pymongo import MongoClient
    import bson.objectid                # from bson.objectid import ObjectId
    HAS_MONGO = True
except ImportError:
    HAS_MONGO = False


class MongoDB(object):
    """
        Class to connect to the database and issue a query (to find) or insert a document.
    """
    def __init__(self):
        """
            Initialize variables
        """
        self.success = True
        self.changed = False
        self.result = dict(ansible_facts={})
        self.cnx = None

    def logon(self, username="root", password=None, host='localhost', protocol='mongodb', **kwargs):
        """
            Connect to a database and authenticate.
        """
        if username and password:
            username = urllib.parse.quote_plus(username)
            password = urllib.parse.quote_plus(password)

        uri = '{}://{}:{}@{}/'.format(protocol, username, password, host)

        try:
            self.cnx = pymongo.MongoClient(uri, **kwargs)
        except pymongo.errors.ConnectionFailure as e:
            self.success = False
            return "Could not connect to MongoDB: %s" % e
        return

    def convert_id(self, result):
        """
             Convert the ObjectId in _id  to a string, to make it convertable to JSON
             {u'_id': ObjectId('5a789a190d0d0e46828e7b3e'), u'name': u'HR_Micro_Seg'}
             Note: find_one() returns either a dictionary (a document)  or None
             we return an empty dictionary instead of None.
        """
        if result:
            if result.get("_id"):
                result["_id"] = str(result["_id"])
            return result
        return dict()

    def find_document(self, database_name=None, collection_name=None, query=None):
        """
            First check if the database name and collection name exist and a query has been supplied,
            error out if they do not. Query the collection, using find_one()
        """
        #
        #   Error checking
        #
        if not query:
            self.success = False
            return "Query must be specified!"

        if database_name not in self.cnx.database_names():
            self.success = False
            return "Database name does not exist!"

        db = self.cnx[database_name]
        if collection_name not in db.collection_names(include_system_collections=False):
            self.success = False
            return "Collection name does not exist!"
        #
        # If searching by ObjectId, the string representation needs be converted
        #
        if query and query.get("_id"):
            query["_id"] = bson.objectid.ObjectId(query["_id"])
        #
        # Issue query
        #
        collection = db[collection_name]
        try:
            result = collection.find_one(query)
        except ValueError:
            self.success = False
            return "Invalid query string"

        self.result["ansible_facts"] = self.convert_id(result)
        return self.result

    def insert_document(self, database_name=None, collection_name=None, document=None):
        """
        Playbook would import JSON in the document: "{{lookup('file','./foo.json')}}"
        Return the _id assigned to the document as an ansible_fact
        """
        db = self.cnx[database_name]
        collection = db[collection_name]
        try:
            result = collection.insert_one(document)
        except:
            self.success = False
            return "Exception inserting document in database collection"

        self.changed = True
        self.result["msg"] = "success"
        self.result["ansible_facts"] = dict(_id=str(result.inserted_id))

        return self.result


def main():
    """
        main() processes and validates parameters, checks for the proper SDK, connects and
        authenticates with the data base and exists.
    """
    module = AnsibleModule(
        argument_spec=dict(
            host=dict(default="localhost", required=False),
            username=dict(default="root", required=False),
            password=dict(default=None, required=False, no_log=True),
            authsource=dict(default="admin", required=False),
            port=dict(default=27017, required=False, type="int"),
            protocol=dict(default="mongodb", required=False, choices=["mongodb", "mongodb+srv"]),
            database=dict(required=True),
            collection=dict(required=True),
            query=dict(required=False, type="dict"),
            document=dict(required=False, type="dict"),
            appname=dict(required=False, default=None),
            tls=dict(required=False, default=False, type="bool"),
            tlscafile=dict(required=False, default=None),
            replicaset=dict(required=False, default=None),
            readpreference=dict(required=False, default="primary", choices=["primary", "primaryPreferred", "secondary", "secondaryPreferred", "nearest"])
        ),
        supports_check_mode=False
    )

    #
    #  Validation
    #
    if not HAS_MONGO:
        module.fail_json(msg="The python mongoDB SDK, pymongo, is required")

    if module.params.get("query") and module.params.get("document"):
        module.fail_json(msg="Specify either query or document")

    #
    #  Build camel case keyword arguments for the client connection request
    #
    client_args = dict(port=module.params.get("port"),
                       authSource=module.params.get("authsource"),
                       replicaSet=module.params.get("replicaset"),
                       readPreference=module.params.get("readpreference"),
                       appname=module.params.get("appname"),
                       tls=module.params.get("tls"),
                       tlsCAFile=module.params.get("tlscafile"))

    #
    #  Connect and authenticate with the data base, these params have default values specified
    #
    mdx = MongoDB()
    result = mdx.logon(username=module.params["username"],
                       password=module.params["password"],
                       host=module.params["host"],
                       protocol=module.params["protocol"],
                       **client_args)

    if not mdx.success:
        module.fail_json(msg=result)

    #
    #  Either insert or find a document in the data base
    #
    if module.params.get("document"):
        result = mdx.insert_document(collection_name=module.params.get("collection"),
                                     database_name=module.params.get("database"),
                                     document=copy.deepcopy(module.params.get("document")))
    else:
        result = mdx.find_document(collection_name=module.params.get("collection"),
                                   database_name=module.params.get("database"),
                                   query=copy.deepcopy(module.params.get("query")))

    if mdx.success:
        module.exit_json(changed=mdx.changed, **result)
    else:
        module.fail_json(msg=result)


try:                                                       # Testing outside Ansible framework
    from ansible_hacking import AnsibleModule              # https://github.com/joelwking/ansible-hacking
    PYCHARM = True
except ImportError:
    from ansible.module_utils.basic import AnsibleModule   # When running inside Ansible framework

if __name__ == "__main__":
    """ Logic for remote debugging with Pycharm Pro
    """

    try:
        PYCHARM
    except NameError:
        pass
    else:
        import pydevd
        import os     # os.getenv("SSH_CLIENT").split(" ")  ['192.168.56.1', '51406', '22']
        pydevd.settrace(os.getenv("SSH_CLIENT").split(" ")[0], stdoutToServer=True, stderrToServer=True)

    main()
