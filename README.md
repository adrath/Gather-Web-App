# Gather
Flask/MySQL web app that lets users create and join events

## Overview
A website that functions as a public event planner, a little bit like Meetup. The website will have Groups and Events that users can join/view. Groups could be a location or area of interest (e.g. SF, AlgorithmsMeetup, Soccer, etc). Each event will be associated with a group. The group will be assigned by the host and host must be part of the group to create the event belonging to the group. Participants must be the part of the same group to join the event. The host will have the ability to create an event that includes a time, place, and a description of the event. They can optionally add other users to the event. All groups and events will be public and viewable to everyone but only users who are registered with the website can create new events/groups or join events/groups. Events will be displayed in the order of most recently occurring to furthest out. Only the host/owner of the event will have the access rights to be able to edit the event. Users who are logged in should be able to view a separate dashboard that lists the events that they hosted or joined. Additionally, each event can have 0 or more tags that users can use to search for an event/group. Tags can be added to events by the hosts or participants of the event.
 
### Quickstart Guide
* `git clone` this repository
* create a new file called `database.py` and populate it with your db info:

```
class Info:
     def __init__(self):
         self.username = 'cs340_username'
         self.password = 'password'
         self.database = 'cs340_username'
         self.host = 'classmysql.engr.oregonstate.edu' 
```

* Create your virtual environment by running: `python3 -m venv env`
* Activate your virtual env: `source env/bin/activate`
* Install packages inside virtual environment:  `pip3 install -r requirements.txt`
* If you haven't already set up database tables for Gather, seed your database with the `SQL/cs340_Gather_db_dump.sql` file.
* Run your application: `python application.py`
* Remember to change your port number in `application.py` if you are on flip. If localhost, use port 8000.
* Deactivate your virtual environment: `deactivate`

* Remember, don't push any passwords or personal info. Don't push your db credentials.
 
## Database Design
Entities are Users, Events, Groups, Tags. Descriptions of each entities, attributes, and its relationships are detailed below:
### Relationships/Constraints:
* User can host 0 or many events. Event should have exactly one host. This is a one-to-many relationship.
* User can participate in 0 or many events. Event can have 0 or many participants. This is an example of many-to-many relationship.
* User cannot be both host and a participant to the same event. They must be either-or.
* Group can have 0 or many users. Users can be part of 0 or many groups. This is another many-to-many relationship.
* Event can be part of exactly one group. Groups can have 0 or many related events (one-to-many).
* Host of an event must be in the group that event is part of. 
* Tag can be associated with 0 or many events. Event can have 0 or many tags. (many-to-many)
 
### Gather_User (Entity)
* Username - unique, not null, varchar 255
* Password - encrypted, not null, varchar 255
* User_ID - Primary key auto incremented

### Gather_Event (Entity)
* Title - not null, varchar 255
* Event_ID - primary key, unique
* Group_ID - foreign key
* Start_Date - not null, date
* Start_Time - not null, time 
* End_Date - optional, date
* End_Time - optional, time
* Location - not null, varchar 255
* Description - optional, varchar 500

### Gather_Tag (Entity)
* Tag_Name - primary key, unique; char 50

### Gather_Group (Entity)
* Group_ID - primary key auto-incremented
* Group_Name - not null varchar 255
 
### G_Group_Member (Relationship between Group and User)
* Group_ID
* User_ID

### G_Event_Host (Relationship between Event and User)
* Event_ID
* Host of the event (User ID)

### G_Event_Participant (Relationship between Event and User)
* Event_ID 
* Participant (User ID) 

### G_Event_Tag (Relationship between Event and Tag)
* Event_ID 
* Tag_Name 
