# Ansible Collection - joelwking.mongodb

This collection packages an Ansible module and associated role which inserts or queries a MongoDB document.

## Module Documentation
You can use the moodule-path argument to view the documentation for a module packaged with the collection
```bash
$ ansible-doc --module-path  /collections/ansible_collections/joelwking/mongodb/plugins/modules/mongodb_iq
```
## Role Documentation
Refer to the `README.md` in the role directory on how to use and call the role. There is a sample playbook in the role in `tests/test.yml` which demonstrates how to use the role. 

## Setting up the Environment
Given your collections is installed on the control node at `/collections/ansible_collections/joelwking` you will need to configure the environment to locate the collection and optionally, the associated role.

```bash
export ANSIBLE_COLLECTIONS_PATHS=/collections/
export ANSIBLE_ROLES_PATH=/collections/ansible_collections/joelwking/mongodb/roles
```
Or update your `ansible.cfg` file to include these values:
```
collections_paths = /collections/
roles_path    = /collections/ansible_collections/joelwking/mongodb/roles
```
Note: you do not need to use the provided role, the module can be called directly from your playbook. The role is is included to provide usage examples and demonstrate that Ansible Collections can also package a role.

## Installing the collection

Use the `ansible-galaxy collection` command to install the collection.

Refer to the `requirements.txt` file for dependencies.

Collection version 0.0.3 has been updated to support Digital Ocean's managed MongoDB service and tested using Python 3.6.9 with:

```
ansible==2.10.7
ansible-base==2.10.5
dnspython==2.1.0
pymongo==3.11.4
```

## Examples

Refer to the following example inventory, vars files and playbook.

### Inventory

`files/inventory.yml`

```yaml
all:
    children:
        mongodb:
            hosts:
              db-mongodb-nyc3-59535-4651b9d2.mongo.ondigitalocean.com:
            vars:
              port: 27017
              ansible_python_interpreter: /home/administrator/ansible210/bin/python
```

### Vars Files

When using a managed MongoDB service, you will also need to download the cluster’s CA certificate to establish TLS encryption between the control node and the cluster.

`files/passwords.yml`

```yaml
---
mongodb:
  username: doadmin
  password: mypassword
```

`files/input.json`

```json
{"message_gbl": {
    "room_name": "Super-NetOps",
    "teams": "https://outlook.office.com/webhook/0ebc95ca-9544354a"}
}
```

### Playbook

```yaml
- name: load and query MongoDB database
  hosts:  mongodb
  connection: local
  gather_facts: false

  vars:
    database: rebar
    collection: foobar
    filename: "{{ playbook_dir }}/files/input.json"

  vars_files:
     - "{{ playbook_dir }}/files/passwords.yml"

  tasks:

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
```

## Author
joel.king@wwt.com GitHub/gitLab: @joelwking