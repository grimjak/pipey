[![Build Status](https://travis-ci.com/grimjak/pipey.png?branch=master)](https://travis-ci.com/grimjak/pipey)


Services

people - source of truth for candatates, employees etc.
roles / recs - for employee roles and prospective roles
locations - info about locations, buildings, rooms, desks, racks etc. shouldn't contain config data just info
projects - high level info about shows, episodes etc. No config data
files? - info about where actual files are, will be etc. allows for files to be moved between different storage types as required
assetsMetadata - information about assets including version numebers etc.
tasks - info about tasks, tasks have start dates, end dates etc.
notes - 
config - store generic items of configuration which can be related to other things
itassets - workstations etc.

relationships - info about relationships between all things


How to deal with shot groups, sequences etc. Are they in projects or in the assetMetadata.
How to deal with inheritance, is this something that is stored as a relationship?
Is the relationship service doing too much?

authentication - use data from people service to authenticate access to Services

Workflows


Locations
* Add new site
* Remove site

Projects
* New project (by type)
* Get projects (of type) - allow nested projects

Files 
* To begin with this could just be a reference to a file on disk, could be extended 

Config
A config is a document of key value settings, needs to be associated with an entity to be configured and a scope
API Hierarchy is entity, scope passed as parameter. i.e. http://config/moviegeneration?project=TST@sequence=sequence
This would get uids for TST and seq from the project service then check the relationship service to find related config uids
finally returning the appropriate config from the config service.  Is the relationship service overkill for this?

API gateways - Single api calling multiple services 


Example Workflows
* Assign person to desk
*