# Ansible Collection - joelwking.mongodb

Documentation for the collection.

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

## Module Documentation

You can use the moodule-path argument to view the documentation for a module packaged with the collection

$ ansible-doc --module-path  /collections/ansible_collections/joelwking/mongodb/plugins/modules/ mongodb_iq

## Setting up the Environment

Given your collections is at `/collections/ansible_collections/joelwking`

```bash
export ANSIBLE_COLLECTIONS_PATHS=/collections/
```
Or update your `ansible.cfg` file to include

```
collections_paths = /collections/
```