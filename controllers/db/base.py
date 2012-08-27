# -*- coding: utf-8 -*-

__author__ = 'nezuvian';

class base_controller:
    """
    Abstract controller base class
    """

#    User handling
    def create_user(self):
        pass

    def read_user(self, id):
        pass

    def update_user(self, id):
        pass

    def delete_user(self, id):
        pass

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