-- Authors: Jennifer Kim, Alexander Drath
-- CS340 Database Project Group 20
-- Gather Database SQL Queries


-- get user_id of user with username and password
SELECT user_id FROM gather_user WHERE username=:username AND password=:password;


-- get all events that a user with user_id is hosting
SELECT e.event_id, e.title, e.start_date, e.start_time FROM gather_event e
INNER JOIN g_event_host eh ON e.event_id=eh.event_id
WHERE eh.host_id=:user_id AND e.start_date >= CURDATE()
ORDER BY e.start_date, e.start_time;

-- get ALL events that a user with user_id hosting/hosted
SELECT e.event_id, e.title, e.start_date, e.start_time FROM gather_event e
INNER JOIN g_event_host eh ON e.event_id=eh.event_id
WHERE eh.host_id=:user_id
ORDER BY e.start_date DESC, e.start_time DESC;


-- get all upcoming events that a user with user_id is participating
SELECT e.event_id, e.title, e.start_date, e.start_time FROM gather_event e
INNER JOIN g_event_participant ep ON e.event_id=ep.event_id
WHERE ep.participant_id=:user_id AND e.start_date >= CURDATE()
ORDER BY e.start_date, e.start_time;

-- get ALL events that a user with user_id participated/participating
SELECT e.event_id, e.title, e.start_date, e.start_time FROM gather_event e
INNER JOIN g_event_participant ep ON e.event_id=ep.event_id
WHERE ep.participant_id=:user_id
ORDER BY e.start_date DESC, e.start_time DESC;

-- return a row if the user is a member of the group that event is part of
SELECT gm.group_id FROM g_group_member gm INNER JOIN gather_event e
ON e.group_id=gm.group_id WHERE gm.member_id=:user_id AND e.event_id=:event_id;

-- get list of all upcoming events in the order of most recently happening to furthest out
SELECT event_id, title, start_date, start_time, location, description
FROM gather_event WHERE start_date >= CURDATE()
ORDER BY start_date ASC, start_time ASC;

-- get list of all upcoming events and its tags in the order of most recently happening to furthest out
SELECT e.event_id, title, start_date, start_time, location, description, tag_name
FROM gather_event e LEFT JOIN g_event_tag t ON e.event_id=t.event_id
WHERE start_date >= CURDATE()
ORDER BY start_date ASC, start_time ASC;

-- get list of ALL events in the order of most recent to oldest
SELECT event_id, title, start_date, start_time, location, description
FROM gather_event ORDER BY start_date DESC, start_time DESC;


-- get list of all groups in alphabetical order
SELECT group_name FROM `gather_group` ORDER BY group_name;

-- get list of all groups a user with user_id is part of
SELECT g.group_id, group_name FROM gather_group g INNER JOIN
g_group_member gm ON g.group_id=gm.group_id
WHERE gm.member_id=:user_id;

-- get list of all upcoming events in a certain group
SELECT e.event_id, e.title, e.start_date, e.start_time, e.location
FROM gather_event e INNER JOIN gather_group g ON g.group_id=e.group_id
WHERE start_date >= CURDATE() AND g.group_id=:group_id
ORDER BY e.start_date ASC, e.start_time ASC;

-- get list of all events in a certain group
SELECT e.event_id, e.title, e.start_date, e.start_time, e.location
FROM gather_event e INNER JOIN gather_group g ON g.group_id=e.group_id
WHERE g.group_name=:group_name
ORDER BY e.start_date DESC, e.start_time DESC;

-- get list of all members of a group
SELECT m.username FROM g_group_member gm INNER JOIN gather_user m ON gm.member_id=m.user_id
WHERE group_id=:group_id;


-- get list of all tags
SELECT * FROM gather_tag;


-- get list of all UPCOMING events with a certain tag
SELECT t.tag_name, e.event_id, e.title, e.start_date, e.start_time
FROM gather_tag t INNER JOIN g_event_tag et
ON t.tag_name=et.tag_name
INNER JOIN gather_event e ON e.event_id=et.event_id
WHERE t.tag_name=:tag_name AND e.start_date >= curdate()
ORDER BY e.start_date, e.start_time;

-- get list of ALL events with a certain tag
SELECT t.tag_name, e.event_id, e.title, e.start_date, e.start_time
FROM gather_tag t INNER JOIN g_event_tag et
ON t.tag_name=et.tag_name
INNER JOIN gather_event e ON e.event_id=et.event_id
WHERE t.tag_name=:tag_name
ORDER BY e.start_date DESC, e.start_time DESC;


-- get details on a particular event with event_id
SELECT e.event_id, e.title, e.start_date, e.start_time, e.end_date, e.end_time, e.location, e.description, g.group_name
FROM gather_event e INNER JOIN gather_group g ON e.group_id=g.group_id
WHERE event_id=:event_id;

-- get all tags of a particular event with event_id
SELECT t.tag_name FROM gather_tag t
INNER JOIN g_event_tag et ON t.tag_name=et.tag_name
INNER JOIN gather_event e ON e.event_id=et.event_id
WHERE e.event_id=:event_id

-- get the host's username of a particular event with event_id
SELECT h.host_id, u.username FROM g_event_host h
INNER JOIN gather_event e ON e.event_id=h.event_id
INNER JOIN gather_user u ON u.user_id=h.host_id
WHERE e.event_id=:event_id;

-- get the username of all participants of a particular event with event_id
SELECT p.participant_id, u.username FROM g_event_participant p
INNER JOIN gather_event e ON e.event_id=p.event_id
INNER JOIN gather_user u ON u.user_id=p.participant_id
WHERE e.event_id=:event_id;



-- add a new user
INSERT INTO gather_user (username, password) VALUES (:username, :password);

-- add a new tag
INSERT INTO gather_tag (tag_name) VALUES (:tag_name);

-- add a new group
INSERT INTO gather_group (group_name) VALUES (:group_name);

-- add a new event
INSERT INTO gather_event (title, group_id, start_date, start_time, end_date, end_time, location, description)
VALUES (:title, :group_id, :start_date, :start_time, :end_date, :end_time, :location, :description);

-- add a new tag to an event
INSERT INTO g_event_tag (event_id, tag_name) VALUES (:event_id, :tag_name);

-- add a host for an event ** This needs to happen right after creating a new event
INSERT INTO g_event_host (event_id, host_id) VALUES (:event_id, :host_id);

-- add a new participant for an event
INSERT INTO g_event_participant (event_id, participant_id) VALUES (:event_id, :participant_id);

-- add a new member to a group
INSERT INTO g_group_member (group_id, member_id) VALUES (:group_id, :member_id);


-- update event 
UPDATE gather_event SET 
title=:title, start_date=:start_date, start_time=:start_time, 
end_date=:end_date, end_time=:end_time, l
ocation=:location, description=:description
WHERE event_id=:event_id


-- remove a tag from an event
DELETE FROM g_event_tag WHERE tag_name=:tag_name and event_id=:event_id;

-- delete an event
DELETE FROM gather_event WHERE event_id=:event_id;

-- remove a participant from an event
DELETE FROM g_event_participant WHERE event_id=:event_id AND participant_id=user_id;