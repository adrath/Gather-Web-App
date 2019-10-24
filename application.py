import os, sys, datetime

from datetime import datetime
from flask_mysqldb import MySQL
from flask import Flask, flash, session, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from database import *
from utils import *

app = Flask(__name__)

# random string generator to encrypt the cookie
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# MySQL configurations
info = Info()
app.config['MYSQL_USER'] = info.username
app.config['MYSQL_PASSWORD'] = info.password
app.config['MYSQL_DB'] = info.database
app.config['MYSQL_HOST'] = info.host
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
@check_user_login
def index(username, user_id):
    """ Route for Index (homepage) """

    cur = mysql.connection.cursor()
    # get a list of all upcoming events and its tags in the order of most recently happening to furthest out
    sql_query = 'SELECT e.event_id, title, start_date, start_time, location, description, tag_name ' \
                'FROM gather_event e LEFT JOIN g_event_tag t ON e.event_id=t.event_id ' \
                'WHERE start_date >= CURDATE() ' \
                'ORDER BY start_date ASC, start_time ASC'

    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()

    eventDict = {}

    for event in rows:
        if event['event_id'] not in eventDict:
            eventDict[event['event_id']] = {}
            eventDict[event['event_id']]['info'] = event
            eventDict[event['event_id']]['tags'] = set()
        eventDict[event['event_id']]['tags'].add(event['tag_name'])

    return render_template('index.html', username=username, events=eventDict)

@app.route('/search', methods=['POST'])
@check_user_login
def sort_by(username, user_id):
    """ Route for Index (homepage) """
    
    if request.method == 'POST':
        title = request.form['title'] if request.form['title'] else None
        start_date = request.form['start_date'] if request.form['start_date'] else None
        location = request.form['location'] if request.form['location'] else None
	
        if title and start_date is None and location is None:
            cur = mysql.connection.cursor()
            # get a list of all upcoming events and its tags in the order of most recently happening to furthest out
            sql_query = 'SELECT e.event_id, title, start_date, start_time, location, description, tag_name ' \
                        'FROM gather_event e LEFT JOIN g_event_tag t ON e.event_id=t.event_id ' \
                        'WHERE title LIKE %s ' \
                        'ORDER BY start_date ASC, start_time ASC'
            cur.execute(sql_query, ("%" + title + "%",))
            rows = cur.fetchall()
            cur.close()

            eventDict = {}

            for event in rows:
                if event['event_id'] not in eventDict:
                    eventDict[event['event_id']] = {}
                    eventDict[event['event_id']]['info'] = event
                    eventDict[event['event_id']]['tags'] = set()
                eventDict[event['event_id']]['tags'].add(event['tag_name'])

            if eventDict is None:
                flash("Unable to find a result")
                return redirect(url_for('index'))
            
        elif title is None and start_date and location is None:
            cur = mysql.connection.cursor()
            # get a list of all upcoming events and its tags in the order of most recently happening to furthest out
            sql_query = 'SELECT e.event_id, title, start_date, start_time, location, description, tag_name ' \
                        'FROM gather_event e LEFT JOIN g_event_tag t ON e.event_id=t.event_id ' \
                        'WHERE start_date=%s ' \
                        'ORDER BY start_date ASC, start_time ASC'
            cur.execute(sql_query, (start_date,))
            rows = cur.fetchall()
            cur.close()

            eventDict = {}

            for event in rows:
                if event['event_id'] not in eventDict:
                    eventDict[event['event_id']] = {}
                    eventDict[event['event_id']]['info'] = event
                    eventDict[event['event_id']]['tags'] = set()
                eventDict[event['event_id']]['tags'].add(event['tag_name'])

            if eventDict is None:
                flash("Unable to find a result")
                return redirect(url_for('index'))

        elif title is None and start_date is None and location:
            cur = mysql.connection.cursor()
            # get a list of all upcoming events and its tags in the order of most recently happening to furthest out
            sql_query = 'SELECT e.event_id, title, start_date, start_time, location, description, tag_name ' \
                        'FROM gather_event e LEFT JOIN g_event_tag t ON e.event_id=t.event_id ' \
                        'WHERE location LIKE %s ' \
                        'ORDER BY start_date ASC, start_time ASC'
            cur.execute(sql_query, ("%" + location + "%",))
            rows = cur.fetchall()
            cur.close()

            eventDict = {}

            for event in rows:
                if event['event_id'] not in eventDict:
                    eventDict[event['event_id']] = {}
                    eventDict[event['event_id']]['info'] = event
                    eventDict[event['event_id']]['tags'] = set()
                eventDict[event['event_id']]['tags'].add(event['tag_name'])

            if eventDict is None:
                flash("Unable to find a result")
                return redirect(url_for('index'))
            
        elif title and start_date and location is None:
            cur = mysql.connection.cursor()
            # get a list of all upcoming events and its tags in the order of most recently happening to furthest out
            sql_query = 'SELECT e.event_id, title, start_date, start_time, location, description, tag_name ' \
                        'FROM gather_event e LEFT JOIN g_event_tag t ON e.event_id=t.event_id ' \
                        'WHERE title LIKE %s AND start_date=%s ' \
                        'ORDER BY start_date ASC, start_time ASC'
            cur.execute(sql_query, ("%" + title + "%", start_date))
            rows = cur.fetchall()
            cur.close()

            eventDict = {}

            for event in rows:
                if event['event_id'] not in eventDict:
                    eventDict[event['event_id']] = {}
                    eventDict[event['event_id']]['info'] = event
                    eventDict[event['event_id']]['tags'] = set()
                eventDict[event['event_id']]['tags'].add(event['tag_name'])

            if eventDict is None:
                flash("Unable to find a result")
                return redirect(url_for('index'))
            
        elif title is None and start_date and location:
            cur = mysql.connection.cursor()
            # get a list of all upcoming events and its tags in the order of most recently happening to furthest out
            sql_query = 'SELECT e.event_id, title, start_date, start_time, location, description, tag_name ' \
                        'FROM gather_event e LEFT JOIN g_event_tag t ON e.event_id=t.event_id ' \
                        'WHERE start_date=%s AND location LIKE %s ' \
                        'ORDER BY start_date ASC, start_time ASC'
            cur.execute(sql_query, (start_date, "%" + location + "%"))
            rows = cur.fetchall()
            cur.close()

            eventDict = {}

            for event in rows:
                if event['event_id'] not in eventDict:
                    eventDict[event['event_id']] = {}
                    eventDict[event['event_id']]['info'] = event
                    eventDict[event['event_id']]['tags'] = set()
                eventDict[event['event_id']]['tags'].add(event['tag_name'])

            if eventDict is None:
                flash("Unable to find a result")
                return redirect(url_for('index'))
            
        elif title and start_date is None and location:
            cur = mysql.connection.cursor()
            # get a list of all upcoming events and its tags in the order of most recently happening to furthest out
            sql_query = 'SELECT e.event_id, title, start_date, start_time, location, description, tag_name ' \
                        'FROM gather_event e LEFT JOIN g_event_tag t ON e.event_id=t.event_id ' \
                        'WHERE title LIKE %s AND location LIKE %s ' \
                        'ORDER BY start_date ASC, start_time ASC'
            cur.execute(sql_query, ("%" + title + "%", "%" + location + "%"))
            rows = cur.fetchall()
            cur.close()

            eventDict = {}

            for event in rows:
                if event['event_id'] not in eventDict:
                    eventDict[event['event_id']] = {}
                    eventDict[event['event_id']]['info'] = event
                    eventDict[event['event_id']]['tags'] = set()
                eventDict[event['event_id']]['tags'].add(event['tag_name'])

            if eventDict is None:
                flash("Unable to find a result")
                return redirect(url_for('index'))
        
        elif title and start_date and location:
            cur = mysql.connection.cursor()
            # get a list of all upcoming events and its tags in the order of most recently happening to furthest out
            sql_query = 'SELECT e.event_id, title, start_date, start_time, location, description, tag_name ' \
                        'FROM gather_event e LEFT JOIN g_event_tag t ON e.event_id=t.event_id ' \
                        'WHERE title LIKE %s AND start_date=%s AND location LIKE %s ' \
                        'ORDER BY start_date ASC, start_time ASC'
            cur.execute(sql_query, ("%" + title + "%", start_date, "%" + location + "%"))
            rows = cur.fetchall()
            cur.close()

            eventDict = {}

            for event in rows:
                if event['event_id'] not in eventDict:
                    eventDict[event['event_id']] = {}
                    eventDict[event['event_id']]['info'] = event
                    eventDict[event['event_id']]['tags'] = set()
                eventDict[event['event_id']]['tags'].add(event['tag_name'])

            if eventDict is None:
                flash("Unable to find a result")
                return redirect(url_for('index'))
        
        else:
            return redirect(url_for('index'))
        
        return render_template('index.html', username=username, events=eventDict)

@app.route('/events/event', methods=['GET', 'POST'])
@check_user_login
def event(username, user_id):
    """ Route for displaying details of one event """
    # Get the event ID from the request params
    event_id = int(request.args.get("eid"))

    # Get the event details from DB
    cur = mysql.connection.cursor()
    sql_query = 'SELECT e.event_id, e.title, e.start_date, e.start_time, e.end_date, e.end_time, ' \
                'e.location, e.description, g.group_id, g.group_name FROM gather_event e INNER JOIN gather_group g ' \
                'ON e.group_id=g.group_id WHERE event_id=%s'
    cur.execute(sql_query, (event_id,))
    event = cur.fetchone()
    cur.close()

    # Get the host id of the event
    cur = mysql.connection.cursor()
    sql_query = 'SELECT h.host_id, u.username FROM g_event_host h \
                INNER JOIN gather_event e ON e.event_id=h.event_id \
                INNER JOIN gather_user u ON u.user_id=h.host_id \
                WHERE e.event_id=%s'
    cur.execute(sql_query, (event_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        flash("Host not found")
        return render_template("error.html")

    host = {
        'host_name': row['username'],
        'host_id': row['host_id']
    }

    # Get all participants from the event
    cur = mysql.connection.cursor()
    sql_query = 'SELECT p.participant_id, u.username FROM g_event_participant p \
                INNER JOIN gather_event e ON e.event_id=p.event_id \
                INNER JOIN gather_user u ON u.user_id=p.participant_id \
                WHERE e.event_id=%s'
    cur.execute(sql_query, (event_id,))
    rows = cur.fetchall()
    cur.close()

    participants = {}

    for r in rows:
        participants[r['participant_id']] = r['username']

    # Get all the tags associated with the event
    cur = mysql.connection.cursor()
    sql_query = 'SELECT t.tag_name FROM gather_tag t \
                INNER JOIN g_event_tag et ON t.tag_name=et.tag_name \
                INNER JOIN gather_event e ON e.event_id=et.event_id \
                WHERE e.event_id=%s'
    cur.execute(sql_query, (event_id,))
    rows = cur.fetchall()
    cur.close()

    eventTags = []

    # Store SQL reult as a list of (dict) event tags
    for r in rows:
        eventTags.append(r)

    # Get all the tags possible for selection by the user to add
    cur = mysql.connection.cursor()
    sql_query = 'SELECT t.tag_name FROM gather_tag t \
                WHERE t.tag_name NOT IN \
                (SELECT t.tag_name FROM gather_tag t \
                INNER JOIN g_event_tag et ON t.tag_name=et.tag_name \
                INNER JOIN gather_event e ON e.event_id=et.event_id \
                WHERE e.event_id=%s) \
                ORDER BY t.tag_name'
    cur.execute(sql_query, (event_id,))
    rows = cur.fetchall()
    cur.close()

    tags = []

    # Store SQL result as a list of (dict) tags
    for r in rows:
        tags.append(r)

    if request.method == 'POST':
        tag = request.form['tag_name']

        # Add the tag and event_id into g_event_tag table
        cur = mysql.connection.cursor()
        sql_query = 'INSERT INTO `g_event_tag` (event_id, tag_name) VALUES (%s,%s)'
        cur.execute(sql_query, (event_id, tag,))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('event', eid=event_id))

    return render_template('event.html', username=username, user_id=user_id, event=event, host=host,
                           participants=participants, tags=tags, eventTags=eventTags)


@app.route('/events/new', methods=['GET', 'POST'])
@login_required
def addEvent(username, user_id):
    """ Route for adding new events """
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        # Get only groups that the user is part of
        sql_query = 'SELECT g.group_id, group_name FROM gather_group g INNER JOIN \
                     g_group_member gm ON g.group_id=gm.group_id \
                     WHERE gm.member_id=%s ORDER BY group_name'
        cur.execute(sql_query, (user_id,))
        rows = cur.fetchall()
        cur.close()

        groups = []

        # Store SQL result as a list of (dict) groups
        for r in rows:
            groups.append(r)

        return render_template('newEvent.html', username=username, groups=groups)

    elif request.method == 'POST':
        title = request.form['title']
        group = request.form['group_id']
        start_date = request.form['start_date']
        start_time = request.form['start_time']
        end_date = request.form['end_date'] if request.form['end_date'] else None
        end_time = request.form['end_time'] if request.form['end_time'] else None
        location = request.form['location']
        description = request.form['description'] if request.form['description'] else None

        eventTime = datetime.strptime(start_date, '%Y-%m-%d').date()
        today = datetime.today().date()

        if eventTime < today:
            flash("You cannot add an event that starts in the past!")
            return redirect(url_for('addEvent'))

        if not title or not group or not start_date or not start_time or not location:
            flash("Invalid input")
            return redirect(url_for('addEvent'))

        # if valid input, insert into group table in the db
        cur = mysql.connection.cursor()
        sql_query = 'INSERT INTO gather_event (title, group_id, start_date, start_time, end_date, end_time, location, description) \
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        cur.execute(sql_query, (title, group, start_date, start_time, end_date, end_time, location, description))
        mysql.connection.commit()
        cur.close()

        # Get the event ID of the event created
        cur = mysql.connection.cursor()
        sql_query = 'SELECT event_id FROM gather_event WHERE title=%s AND group_id=%s'
        cur.execute(sql_query, (title, group,))
        row = cur.fetchone()
        cur.close()

        # Add the user as the host to the event created
        cur = mysql.connection.cursor()
        sql_query = "INSERT INTO `g_event_host` (event_id, host_id) VALUES (%s,%s)"
        cur.execute(sql_query, (row['event_id'], user_id,))
        mysql.connection.commit()
        cur.close()

        flash("Successfully created a new event called " + title + "!")
        return redirect(url_for('index'))


@app.route('/events/event/join', methods=['POST'])
@login_required
def joinEvent(username, user_id):
    """ Route for joining an event """
    if not username:
        flash("Please login first")
        return redirect(url_for('login'))

    # Get the event ID from the hidden form value
    event_id = int(request.form['eid'])

    # Check if the user is part of the group that event is in
    cur = mysql.connection.cursor()
    sql_query = 'SELECT gm.group_id FROM g_group_member gm INNER JOIN gather_event e \
                 ON e.group_id=gm.group_id WHERE gm.member_id=%s AND e.event_id=%s'
    cur.execute(sql_query, (user_id, event_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        flash("You must be part of the group to join this event.")
        return redirect(url_for("groups"))

    # Add user to the event participant
    cur = mysql.connection.cursor()
    sql_query = 'INSERT INTO g_event_participant (event_id, participant_id) VALUES (%s, %s)'
    cur.execute(sql_query, (event_id, user_id,))
    mysql.connection.commit()
    cur.close()

    flash("Successfully joined event!")
    return redirect(url_for('dashboard'))


@app.route('/events/event/update', methods=['GET', 'POST'])
@login_required
def updateEvent(username, user_id):
    """ Route to update an existing event """

    # Get the event ID from the request params
    event_id = int(request.args.get("eid"))

    # Get the host id of the event
    cur = mysql.connection.cursor()
    sql_query = 'SELECT h.host_id, u.username FROM g_event_host h \
                            INNER JOIN gather_event e ON e.event_id=h.event_id \
                            INNER JOIN gather_user u ON u.user_id=h.host_id \
                            WHERE e.event_id=%s'
    cur.execute(sql_query, (event_id,))
    row = cur.fetchone()
    cur.close()

    # If no host is found
    if not row: return render_template("error.html")

    # Check for user permission
    if row['host_id'] != user_id:
        flash("You do not have permissions to edit this event")
        return redirect(url_for("index"))

    # Get the event details from DB
    cur = mysql.connection.cursor()
    sql_query = 'SELECT e.event_id, e.title, e.start_date, e.start_time, e.end_date, e.end_time, ' \
                'e.location, e.description, g.group_id, g.group_name FROM gather_event e INNER JOIN gather_group g ' \
                'ON e.group_id=g.group_id WHERE event_id=%s'
    cur.execute(sql_query, (event_id,))
    event = cur.fetchone()
    cur.close()

    # Get all participants from the event
    cur = mysql.connection.cursor()
    sql_query = 'SELECT p.participant_id, u.username FROM g_event_participant p \
                     INNER JOIN gather_event e ON e.event_id=p.event_id \
                     INNER JOIN gather_user u ON u.user_id=p.participant_id \
                     WHERE e.event_id=%s'
    cur.execute(sql_query, (event_id,))
    rows = cur.fetchall()
    cur.close()

    participants = {}
    for r in rows: participants[r['participant_id']] = r['username']

    if request.method == 'GET':
        return render_template("editEvent.html", username=username, event=event, participants=participants)

    else:
        # Get updated info from the form submitted via POST request
        title = request.form['title'] if request.form['title'] else event['title']
        start_date = request.form['start_date'] if request.form['start_date'] else event['start_date']
        start_time = request.form['start_time'] if request.form['start_time'] else event['start_time']
        end_date = request.form['end_date'] if request.form['end_date'] else event['end_date']
        end_time = request.form['end_time'] if request.form['end_time'] else event['end_time']
        location = request.form['location'] if request.form['location'] else event['location']
        description = request.form['description'] if request.form['description'] else event['description']

        eventTime = datetime.strptime(start_date, '%Y-%m-%d').date()
        today = datetime.today().date()

        if eventTime < today:
            flash("You cannot add an event that starts in the past!")
            return redirect(url_for('addEvent'))

        if not title or not group or not start_date or not start_time or not location:
            flash("Invalid update")
            return redirect(url_for('dashboard'))

        # Update event in DB
        cur = mysql.connection.cursor()
        sql_query = 'UPDATE gather_event SET \
                            title=%s, start_date=%s, start_time=%s, \
                            end_date=%s, end_time=%s, location=%s, description=%s \
                            WHERE event_id=%s'
        cur.execute(sql_query, (title, start_date, start_time, end_date, end_time, location, description, event_id,))
        mysql.connection.commit()
        cur.close()

        flash("Success")
        return redirect(url_for("index"))

    
@app.route('/events/event/delete', methods=['POST'])
@login_required
def removeEventFromEvent(username, user_id):
    eid = request.form['eid']

    cur = mysql.connection.cursor()
    sql_query = "DELETE FROM gather_event WHERE event_id=%s"
    cur.execute(sql_query, (eid,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('dashboard'))
    

@app.route('/groups', methods=['GET', 'POST'])
@check_user_login
def groups(username, user_id):
    """ Route for displaying a list of all groups in Gather """

    cur = mysql.connection.cursor()
    sql_query = 'SELECT group_id, group_name FROM `gather_group` ORDER BY group_name'
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()

    groups = []

    # Store SQL result as a list of (dict) groups
    for r in rows:
        groups.append(r)

    # Now get a list of all groups that user is already part of.
    cur = mysql.connection.cursor()
    sql_query = 'SELECT g.group_id FROM gather_group g INNER JOIN g_group_member gm ' \
                'ON g.group_id=gm.group_id WHERE gm.member_id=%s'
    cur.execute(sql_query, (user_id,))
    rows = cur.fetchall()
    cur.close()

    user_groups = set()
    for r in rows:
        user_groups.add(r['group_id'])

    return render_template('groups.html', username=username, groups=groups, user_groups=user_groups)


@app.route('/groups/group')
@check_user_login
def group(username, user_id):
    """ Route for displaying a list of all events and members associated with a group """

    # Get the group ID from the request params
    group_id = int(request.args.get("gid"))

    # Get the group name
    cur = mysql.connection.cursor()
    sql_query = 'SELECT group_name FROM gather_group WHERE group_id=%s'
    cur.execute(sql_query, (group_id,))
    row = cur.fetchone()
    cur.close()

    if not row:
        return render_template("error.html")

    group_name = row['group_name']

    # Get the group details from DB
    cur = mysql.connection.cursor()
    sql_query = 'SELECT g.group_name, e.event_id, e.title, e.start_date, e.start_time, e.location, e.description ' \
                'FROM gather_event e INNER JOIN gather_group g ON g.group_id=e.group_id ' \
                'WHERE g.group_id=%s ' \
                'ORDER BY e.start_date ASC, e.start_time ASC'
    cur.execute(sql_query, (group_id,))
    rows = cur.fetchall()
    cur.close()

    group_events = []

    for r in rows:
        group_events.append(r)

    # Get list of all members associated with the group
    cur = mysql.connection.cursor()
    sql_query = 'SELECT m.username FROM g_group_member gm INNER JOIN gather_user m ' \
                'ON gm.member_id=m.user_id WHERE group_id=%s'
    cur.execute(sql_query, (group_id,))
    rows = cur.fetchall()
    cur.close()

    members = set()
    for r in rows:
        members.add(r['username'])

    return render_template('group.html', username=username, group_name=group_name, group_id=group_id,
                           group_events=group_events,
                           members=members)


@app.route('/groups/group/join', methods=['POST'])
@login_required
def joinGroup(username, user_id):
    """ Route for joining a group """
    if not username:
        flash("Please login first")
        return redirect(url_for('login'))

    # Get the group ID from the hidden form value
    group_id = int(request.form['gid'])

    # Check if the group exists and user if not already in the group
    cur = mysql.connection.cursor()
    sql_query = 'SELECT * FROM g_group_member WHERE group_id=%s AND member_id=%s'
    cur.execute(sql_query, (user_id, group_id,))
    row = cur.fetchone()
    cur.close()

    if row:
        flash("Error joining group")
        return redirect(url_for('groups'))

    # Add user to the group
    cur = mysql.connection.cursor()
    sql_query = 'INSERT INTO g_group_member (group_id, member_id) VALUES (%s, %s)'
    cur.execute(sql_query, (group_id, user_id,))
    mysql.connection.commit()
    cur.close()

    flash("Successfully joined group!")
    return redirect(url_for('groups'))


@app.route('/groups/new', methods=['GET', 'POST'])
@login_required
def addGroup(username, user_id):
    """ Route for adding a new group """

    if not username:
        flash("Please login first")
        return redirect(url_for('login'))

    if request.method == 'POST':
        newGroup = request.form['group_name']

        if not newGroup:
            flash("Invalid input")
            return redirect(url_for('addGroup'))

        # Check if group_name is already in use
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM `gather_group` WHERE group_name = %s', (newGroup,))
        result = cur.fetchone()
        cur.close()

        if result:
            flash("The group name already exists. Please enter another group name.")
            return render_template('newGroup.html', username=username)

        # if valid input, insert into group table in the db
        cur = mysql.connection.cursor()
        sql_query = 'INSERT INTO `gather_group`(group_name) VALUES (%s)'
        cur.execute(sql_query, (newGroup,))
        mysql.connection.commit()
        cur.close()

        # Get the group_id of the group created
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM `gather_group` WHERE group_name = %s', (newGroup,))
        result = cur.fetchone()
        cur.close()

        if not result:
            return render_template('error.html')

        # Add user to the group
        cur = mysql.connection.cursor()
        sql_query = 'INSERT INTO g_group_member (group_id, member_id) VALUES (%s, %s)'
        cur.execute(sql_query, (result['group_id'], user_id,))
        mysql.connection.commit()
        cur.close()

        flash("Successfully created a new group called " + newGroup + "!")
        return redirect(url_for('groups'))

    return render_template('newGroup.html', username=username)


@app.route('/tags')
@check_user_login
def tags(username, user_id):
    """ Route for displaying a list of all tags in Gather """

    # Get a list of tags from DB
    cur = mysql.connection.cursor()
    sql_query = 'SELECT tag_name FROM `gather_tag` ORDER BY tag_name'
    cur.execute(sql_query)
    rows = cur.fetchall()
    cur.close()

    tags = []

    # Store SQL result as a list of groups
    for r in rows:
        tags.append(r)

    return render_template('tags.html', username=username, tags=tags)


@app.route('/tags/tag')
@check_user_login
def tag(username, user_id):
    """ Route for displaying a list of all events associated with one tag """

    # Get the tag from the request params
    tag_name = request.args.get("tag")

    # Get a list of all events associated with the tag, most recent event first
    cur = mysql.connection.cursor()
    sql_query = 'SELECT t.tag_name, e.event_id, e.title, e.start_date, e.start_time FROM gather_tag t ' \
                'INNER JOIN g_event_tag et ON t.tag_name=et.tag_name INNER JOIN gather_event e ' \
                'ON e.event_id=et.event_id WHERE t.tag_name=%s ' \
                'ORDER BY e.start_date DESC, e.start_time DESC'
    cur.execute(sql_query, (tag_name,))
    rows = cur.fetchall()
    cur.close()

    events = []

    for r in rows:
        events.append(r)

    return render_template('tag.html', username=username, events=events, tag=tag_name)


@app.route('/tags/new', methods=['POST'])
@login_required
def addTag(username, user_id):
    """ Route for adding a new tag name """
    if not username:
        flash("Please login first")
        return redirect(url_for('login'))

    if request.method == 'POST':
        newTag = request.form['tag_name']

        # Check if tag_name is already in use
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM `gather_tag` WHERE tag_name = %s', (newTag,))
        result = cur.fetchone()
        cur.close()

        if result:
            flash("The tag name already exists. Please enter another tag name.")
            return redirect(url_for('tags'))

        # if valid input, insert into tags table in the db
        cur = mysql.connection.cursor()
        sql_query = 'INSERT INTO `gather_tag`(tag_name) VALUES (%s)'
        cur.execute(sql_query, (newTag,))
        mysql.connection.commit()
        cur.close()

        flash("Successfully created a new tag called " + newTag + "!")
        return redirect(url_for('tags'))

    return render_template('error.html')


@app.route('/events/event/tag/delete', methods=['POST'])
@login_required
def removeTagFromEvent(username, user_id):
    tag_name = request.form['tag_name']
    eid = request.form['eid']

    cur = mysql.connection.cursor()
    sql_query = "DELETE FROM g_event_tag WHERE tag_name=%s and event_id=%s"
    cur.execute(sql_query, (tag_name, eid))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('event', eid=eid))


@app.route('/events/event/participant/delete', methods=['POST'])
@login_required
def removeParticipant(username, user_id):
    pid = request.form['pid']
    eid = request.form['eid']

    cur = mysql.connection.cursor()
    sql_query = "DELETE FROM g_event_participant WHERE event_id=%s AND participant_id=%s"
    cur.execute(sql_query, (eid, pid,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('event', eid=eid))


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard(username, user_id):
    """ Route for displaying user's groups and events he/she is hosting or participating """

    # Get a list of all groups that user is part of.
    cur = mysql.connection.cursor()
    sql_query = 'SELECT g.group_id, g.group_name FROM gather_group g INNER JOIN g_group_member gm ' \
                'ON g.group_id=gm.group_id WHERE gm.member_id=%s'
    cur.execute(sql_query, (user_id,))
    groups = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    # get a list of all upcoming events user is hosting in the order of most recently happening to furthest out
    sql_query = 'SELECT e.event_id, title, start_date, start_time ' \
                'FROM gather_event e INNER JOIN g_event_host h ON e.event_id=h.event_id ' \
                'WHERE h.host_id=%s ' \
                'ORDER BY start_date ASC, start_time ASC'

    cur.execute(sql_query, (user_id,))
    host_events = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    # get a list of all upcoming events user is participating in the order of most recently happening to furthest out
    sql_query = 'SELECT e.event_id, title, start_date, start_time ' \
                'FROM gather_event e INNER JOIN g_event_participant p ON e.event_id=p.event_id ' \
                'WHERE p.participant_id=%s ' \
                'ORDER BY start_date ASC, start_time ASC'
    cur.execute(sql_query, (user_id,))
    participating_events = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', username=username, groups=groups, host_events=host_events,
                           participating_events=participating_events)


@app.route('/dashboard/event/delete', methods=['POST'])
@login_required
def removeEventFromDashboard(username, user_id):
    eid = request.form['eid']

    cur = mysql.connection.cursor()
    sql_query = "DELETE FROM gather_event WHERE event_id=%s"
    cur.execute(sql_query, (eid,))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
@check_user_login
def login(username, user_id):
    """ Route for user login """

    if username:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        pw = request.form['password']

        # Get user_id and password matching the username entered
        cur = mysql.connection.cursor()
        cur.execute('SELECT user_id, password FROM gather_user WHERE username = %s', (username,))
        row = cur.fetchone()
        cur.close()

        # If no such username is found
        if not row:
            flash("Please Enter a valid username")
            return render_template('login.html')

        # Verify password
        elif check_password_hash(row['password'], pw):
            session['user_id'] = row['user_id']
            session['user'] = username
            return redirect(url_for('index'))

        # If incorrect password
        else:
            flash("Please Enter a valid password")
            return render_template('login.html')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
@check_user_login
def signup(username, user_id):
    """ Route for user registration """
    if username:
        flash("Please logout First")
        return

    if request.method == 'POST':
        # get user input
        username = request.form['username']
        hashed_pw = generate_password_hash(request.form['password'])

        # validate user input
        if not username or not hashed_pw:
            flash("Please enter a valid username and password")
            return render_template('signup.html')

        # Check if username already exists
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM `gather_user` WHERE username = %s', (username,))
        result = cur.fetchone()
        cur.close()

        if result:
            flash("The username already exists. Please enter another username.")
            return render_template('signup.html')

        # if valid input, insert into users table in the db
        cur = mysql.connection.cursor()
        sql_query = 'INSERT INTO `gather_user`(username, password) VALUES (%s, %s)'
        cur.execute(sql_query, (username, hashed_pw,))
        mysql.connection.commit()
        cur.close()

        flash("Successfully signed up! Please log in to continue")
        return redirect(url_for('login'))

    return render_template('signup.html', username=None)


@app.route('/logout')
def logout():
    """ Route for user logout """
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=sys.argv[1], debug=True)
