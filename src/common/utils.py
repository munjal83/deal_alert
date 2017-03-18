import re

from passlib.hash import pbkdf2_sha512

class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Encrypts the password into pbkdf2_sha512
        :param password: The password from the login/register form
        :return: a pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks the password the user entered matches with that of the database
        The database password is encrypted more than the user password at this stage
        :param password: sha512 hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if password match, false otherwise
        """

        return pbkdf2_sha512.verify(password, hashed_password)