# Ansible Collection - joelwking.mongodb

This document includes notes and tips for creating, building and publishing a collection.

## Creating a new collection

* Create the remote github repository under your organization or username, e.g. joelwking/mongodb
* Create directory on your local machine, e.g. `~/projects/collections/joelwking/`
* Change directory `cd ~/projects/collections/joelwking/`
* Clone the remote repository to your local machine `git clone https://github.com/joelwking/mongodb.git`
* Initialize the collection  `andible-galaxy collection init joelwking.mongodb -f`
* Modify the `galaxy.yml` file.
* Create any additional directories and files.
* Commit and push the changes to the remote directory 

## Modules

* In the `plugins` directory, create the appropriate sub-directory and add your code

## Create role(s) inside the collection

* `cd ~projects//collections/joelwking/mongodb/roles`
* `ansible-galaxy role init mongodb`

## Build the collection

Change your current directory to the root of the collection, for example `cd /collections/ansible_collections/joelwking/mongodb` then issue:
```bash
$ ansible-galaxy collection build
Created collection for joelwking.mongodb at /collections/ansible_collections/joelwking/mongodb/joelwking-mongodb-0.0.1.tar.gz
```

## Upload the collection

```bash
ansible-galaxy collection publish /collections/ansible_collections/joelwking/mongodb/joelwking-mongodb-0.0.1.tar.gz --api-key=SECRET
Publishing collection artifact '/collections/ansible_collections/joelwking/mongodb/joelwking-mongodb-0.0.1.tar.gz' to default https://galaxy.ansible.com/api/
Collection has been published to the Galaxy server default https://galaxy.ansible.com/api/
Waiting until Galaxy import task https://galaxy.ansible.com/api/v2/collection-imports/692 has completed
Collection has been successfully published and imported to the Galaxy server default https://galaxy.ansible.com/api/

```
