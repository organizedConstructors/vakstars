# -*- coding: utf-8 -*-

import sys
import sqlite3
import argparse
# from datetime import date

# TODO: normális dátum kezelés
# TODO: paraméterek ellenőrzése
# TODO: batch kezelés

db = None
c = None
plus_sender = 2
plus_receiver = 10
minus_sender = -1
minus_receiver = -2

def prepare_db():
    """Prepares the database: connect, prepare cursor"""
    global db, c
    db = sqlite3.connect('vakstars.sqlite')
    db.row_factory = sqlite3.Row
    c = db.cursor()

def leave_db():
    """Ends database connection"""
    c.close()

def insert_profile(name, startdate):
    """Inserts a new profile."""
    # TODO: set a sensible startdate as default
    # Check for minimum length
    if len(name) < 3:
        raise Exception('Túl rövid a név!')
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

def vote(sender, receivers, date, reason, type = "1"):
    """File(s) vote(s).

    If the receivers is iterable, everyone in the list will receive a vote.
    """
    if hasattr(receivers, '__iter__'):
        [vote(sender, receiver, date, reason, type) for receiver in receivers]
    else:
        global c, db
        c.execute("""
            INSERT INTO votes(sender, receiver, date, reason, type)
            VALUES (:sender, :receiver, :date, :reason, :type)
            """,
            {'sender': sender, 'receiver': receivers,
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

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def vote_log_to_log_table_html(vote_log):
    """Returns the log table in HTML."""
    for row in reversed(vote_log['vote_log'][-100:]):
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
            reason = html_escape(row['reason'].encode('utf-8'))
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

def help():
    print("""Használat:
    vakstars.py register <név> <dátum>
    vakstars.py vote <+|-> <kitől> <kinek> <dátum> <indoklás>
    vakstars.py vote <+|-> <kitől> [ <fogadó1> <fogadó2> ... ] <dátum> <indoklás>
    vakstars.py dump-log-table
    vakstars.py dump-points-table
        """)

def select_operation(operation):
    operations = ['dump-log-table', 'dump-points-table', 'register', 'vote']
    if operation not in operations:
        raise Exception('Ilyen műveletünk nincs is!')
    else:
        prepare_db()
        if operation == "dump-log-table":
            vote_log_to_log_table_html(get_vote_log())

        if operation == "dump-points-table":
            vote_log_to_points_table_html(get_vote_log())

        if operation == "register":
            name = sys.argv[2].decode('utf-8')
            date = sys.argv[3].decode('utf-8')
            insert_profile(name, date)

        if operation == "vote":
            type = None
            sign = sys.argv[2]
            if sign == "+":
                type = 1
            if sign == "-":
                type = -1

            sender = profile_id_by_name(sys.argv[3].decode('utf-8'))
            if sys.argv[4] != "[":
                receivers = profile_id_by_name(sys.argv[4].decode('utf-8'))
                argument_continue = 5
            else:
                found = False
                found_at = 0
                starting_parameter_index = 5
                i = starting_parameter_index
                while (not found) and (i < len(sys.argv)):
                    if sys.argv[i] == ']':
                        found_at = i
                        found = True
                    i += 1
                if not found:
                    raise Exception('Szintaxishiba: nincsen lezárva a lista!')
                elif found_at == starting_parameter_index:
                    raise Exception('Szintaxishiba: nincsen fogadó fél a listában!')
                else:
                    receivers = sys.argv[starting_parameter_index : found_at]
                    receivers = [profile_id_by_name(s.decode('utf-8')) for s in receivers]
                    argument_continue = found_at + 1

            date = sys.argv[argument_continue].decode('utf-8')
            reason = sys.argv[argument_continue + 1].decode('utf-8')

            vote(sender, receivers, date, reason,type)

        leave_db()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest = "command", help='commands')

    vote_parser = subparsers.add_parser("vote", help="szavazás")
    vote_parser.add_argument("type", help=" <-- típus választás", choices=['+', '-'])
    vote_parser.add_argument("sender", help="<-- küldő neve", type=str) 
    vote_parser.add_argument("receiver", help="<-- fogadó neve", type=str, nargs='+')
    vote_parser.add_argument("date", help="<-- mai dátum (pl. \"2012. 06. 07.\")", type=str)
    vote_parser.add_argument("reason", help="<-- indoklás", type=str)

    register_parser = subparsers.add_parser("register", help="új tag regisztrálása")
    register_parser.add_argument("name", help="<-- új tag neve")
    register_parser.add_argument("date", help="<-- mai dátum (pl. \"2012. 06. 07.\")")

    delete_votes_by_id = subparsers.add_parser("delete_votes_by_id", help="szavazatok törlése azonosító alapján")
    delete_votes_by_id.add_argument("id", help="<-- tag azonosítója", type=int)

    delete_profile = subparsers.add_parser("delete_profile", help="tag törlése azonosító alapján")
    delete_votes_by_id.add_argument("id", help="<-- tag azonosítója", type=int)
	
    args = parser.parse_args()

    if len(sys.argv) == 1:
        help()
    else:
        process = sys.argv[1]

        select_operation(process)
