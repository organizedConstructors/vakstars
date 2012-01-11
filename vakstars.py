#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'scorchio'

import sys
import sqlite3
# from datetime import date

db = None
c = None
plus_sender = 2
plus_receiver = 10
minus_sender = -1
minus_receiver = -2

def prepare_db():
    """Prepares the database: connect, prepare cursor"""
    global db, c
    db = sqlite3.connect('vakstars')
    db.row_factory = sqlite3.Row
    c = db.cursor()

def leave_db():
    """Ends database connection"""
    c.close()

def insert_profile(name, startdate):
    """Inserts a new profile."""
    # TODO: set a sensible startdate as default
    global c, db
    c.execute("""
        INSERT INTO profiles(name, startdate)
        VALUES (:name, :startdate)
        """,
        {'name': name, 'startdate': startdate})
    db.commit()

def delete_votes_by_profile_id(id):
    """Deletes all votes (given and received) for a profile id."""
    global c, db
    c.execute("""
        DELETE FROM votes
        WHERE sender = :id OR receiver = :id
        """, {'id': id})
    db.commit()

def delete_profile(id):
    """Deletes a profile by id."""
    global c, db
    c.execute("""
        DELETE FROM profiles
        WHERE id = :id
        """, {'id': id})
    db.commit()
    delete_votes_by_profile_id(id)

def profile_id_by_name(name):
    """Returns profile id by name."""
    global c
    c.execute("""
        SELECT COUNT(name) AS count FROM profiles
        WHERE name = :name
        """, {'name': name})
    count = c.fetchone()['count']

    if count != 1:
        return None
    else:
        c.execute("""
            SELECT id
            FROM profiles WHERE name = :name
            """, {'name': name})
        return c.fetchone()['id']

def profile_name_by_id(id):
    """Returns name by id."""
    global c
    c.execute("""
            SELECT name
            FROM profiles WHERE id = :id
            """, {'id': id})
    return c.fetchone()['name']

def vote(sender, receiver, date, reason, type = "1"):
    """Files a vote."""
    global c, db
    c.execute("""
        INSERT INTO votes(sender, receiver, date, reason, type)
        VALUES (:sender, :receiver, :date, :reason, :type)
        """,
        {'sender': sender, 'receiver': receiver,
         'date': date, 'reason': reason, 'type': type})
    db.commit()

def get_vote_log():
    """Creates vote log dict from db."""
    global c, db

    votelog = []
    points = {}
    c.execute("""
        SELECT type, sender, receiver, date, reason
        FROM votes
        """)
    for row in c:
        if row["sender"] not in points:
            points[row["sender"]] = 0

        if row["receiver"] not in points:
            points[row["receiver"]] = 0

        sender_original_points = points[row["sender"]]
        receiver_original_points = points[row["receiver"]]

        global plus_sender, plus_receiver, minus_sender, minus_receiver
        if row["type"] == 1:
            points[row["sender"]] += plus_sender
            points[row["receiver"]] += plus_receiver
        if row["type"] == -1:
            points[row["sender"]] += minus_sender
            points[row["receiver"]] += minus_receiver

        vote = {
            'date': row["date"],
            'type': row["type"],
            'sender': row["sender"],
            'receiver': row["receiver"],
            'reason': row["reason"],
            'sender_points_before': sender_original_points,
            'sender_points_after': points[row["sender"]],
            'receiver_points_before': receiver_original_points,
            'receiver_points_after': points[row["receiver"]],
        }
        votelog.append(vote)
    return {'vote_log': votelog, 'points': points}

def vote_log_to_log_table_html(vote_log):
    """Returns the log table in HTML."""
    for row in reversed(vote_log['vote_log']):
        typesign = None
        if row["type"] == 1:
            typesign = "+"
        else:
            typesign = "-"
        print('<tr><td>{date}</td>'\
              '<td>{type}</td>'\
              '<td>{sender} '\
              '({sender_points_before} &rarr; {sender_points_after})</td>'\
              '<td>{receiver} '\
              '({receiver_points_before} &rarr; {receiver_points_after})</td>'\
              '<td>{reason}</td></tr>'.format(
            date = row["date"].encode('utf-8'),
            type = typesign,
            sender = profile_name_by_id(row["sender"]).encode('utf-8'),
            sender_points_before = row["sender_points_before"],
            sender_points_after = row["sender_points_after"],
            receiver = profile_name_by_id(row["receiver"]).encode('utf-8'),
            receiver_points_before = row["receiver_points_before"],
            receiver_points_after = row["receiver_points_after"],
            reason = row['reason'].encode('utf-8')
        ))

def vote_log_to_points_table_html(vote_log):
    """Returns the sorted points table in HTML."""
    sorted_votelog = sorted(
        vote_log['points'].items(),
        key = lambda x: x[1],
        reverse = True
    )
    position = 0
    previous = None
    for profile in sorted_votelog:
        if position == 0 or (previous != None and previous != profile[1]):
            position += 1
        print("{list_position}. {name} - {points}".format(
            list_position = position,
            name = profile_name_by_id(profile[0]).encode('utf-8'),
            points = profile[1]
        ))
        previous = profile[1]

if __name__ == "__main__":
    process = sys.argv[1]

    if process == "dump-log-table":
        prepare_db()
        vl = get_vote_log()
        vote_log_to_log_table_html(vl)
        leave_db()

    if process == "dump-points-table":
        prepare_db()
        vl = get_vote_log()
        vote_log_to_points_table_html(vl)
        leave_db()

    if process == "register":
        prepare_db()
        insert_profile(sys.argv[2].decode('utf-8'), sys.argv[3].decode('utf-8'))
        leave_db()

    if process == "vote":
        prepare_db()
        type = None
        if sys.argv[2] == "+":
            type = 1
        if sys.argv[2] == "-":
            type = -1
        vote(
            profile_id_by_name(sys.argv[3].decode('utf-8')),
            profile_id_by_name(sys.argv[4].decode('utf-8')),
            sys.argv[5].decode('utf-8'), sys.argv[6].decode('utf-8'),
            type
        )
        leave_db()
