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

## Sample Playbook

Refer to `playbooks` directory for sample vars files and playbook.

>Note: You need to download your cluster’s CA certificate (for TLS encryption) between the control node and the cluster. Save the file as `files/ca-certificate.crt` relative to the playbook directory.

## Author
joel.king@wwt.com GitHub/gitLab: @joelwking