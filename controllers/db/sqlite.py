# -*- coding: utf-8 -*-

__author__ = 'nezuvian';

import base
import sys
import sqlite3
import datetime

class sqlite_controller(base.base_controller):
    """
    Controller for sqlite connection
    """

    con = None
    cur = None
    db = None

    def __init__(self, database_name):
        global con, cur, db

        try:
            con = sqlite3.connect(database_name)
            cur = con.cursor()
        except sqlite3.Error, e:
            # todo: log to file
            print "Error %s:" % e.args[0]

    def __del__(self):
        if con:
            con.close()

    #    User handling
    def create_user(self, nickname):
        global con, cur, db
        now = datetime.datetime.now()

        try:
            cur.execute("""
                        INSERT INTO users(nickname, created_at, updated_at)
                        VALUES(:nickname, :now, :now
                        """,
                        {'nickname': nickname, 'now': now}
            )
            con.commit()
            return true
        except sqlite3.Error, e:
            # todo log to file
#            print "Error %s:" % e.args[0]
            return false

    def read_user(self, id):
        global con, cur, db

        try:
            cur.execute("""
                        SELECT * FROM users WHERE users.id = :id
                        """,
                        {'id', id}
            )
            user = cur.fetchone()
        except sqlite3.Error, e:
            # todo log to file
            return false

        return user


    def update_user(self, id, data):
        global con, cur, db

        keys = list(data.keys())
        query = "UPDATE users SET "
        for key in keys:
            query = query+key+"="+data[key]

        query = query+" WHERE users.id=:id"

        try:
            cur.execute(query, {'id': id})
            con.commit()
            return true
        except sqlite3.Error, e:
            # todo log to file
            return false

    def delete_user(self, id):
        global con, cur, db

        try:
            cur.execute("""
                        DELETE FROM users WHERE users.id = :id
                        """,
                    {'id': id}
            )
            con.commit()
            return true
        except sqlite3.Error, e:
        # todo log to file
        #            print "Error %s:" % e.args[0]
            return false

    #   UserInformations handling
    def create_user_information(self, user_id):
        pass

    def readuser_information(self, id):
        pass

    def updateuser_information(self, id):
        pass

    def deleteuser_information(self, id):
        pass

    #    Vote handling
    def create_vote(self, rated_user_id, rating_user_id, vote_type_id):
        pass

    def read_vote(self, id):
        pass

    def update_vote(self, id):
        pass

    def delete_vote(self, id):
        pass

    #    VoteType handling

    def create_vote_type(self):
        pass

    def read_vote_type(self, id):
        pass

    def update_vote_type(self, id):
        pass

    def delete_vote_type(self, id):
        pass

    #    Mixed stuff handling

    def get_all_votes_by_user(self, user_id):
        pass

    def get_all_votes_by_user_with_type(self, user_id, type_id):
        pass

    def get_all_votes_about_user(self, user_id):
        pass

    def get_all_votes_about_user_with_type(self, user_id, type_id):
        pass

    def get_all_votes_by_type(self, type_id):
        pass