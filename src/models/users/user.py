import uuid
import src.models.users.errors as UserErrors
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.constants as UserConstants
from src.models.alerts.alert import Alert


class User(object):

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "User {}".format(self.email)


    @staticmethod
    def is_login_valid(email, password):
        """
        Here the method checks if the email and password sent from the site forms is valid.
        Checks that the email is valid and the password associate with it is correct.
        The method is static as we do not have an user object yet, we check the credentials and then create one.
        :param email: User email
        :param password: a hased sha512 password
        :return: True if valid, False otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION,
                                      query={"email": email})
        if user_data is None:
            #Tell the user that it does not exist
            raise UserErrors.UserNotExistsError("Sorry the user does not exist")

        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was incorrect")

        return True

    @staticmethod
    def register_user(email, password):
        """
        Here the method registers a new user using email and password
        The password is a sha512
        :param email: User email
        :param password: sha512 hashed password
        :return: True if registered successfully, False otherwise
        """

        user_data = Database.find_one(UserConstants.COLLECTION,
                                      query={"email": email})

        if user_data is not None:
            raise UserErrors.UserAlreadyExistsError("The user already exists!")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email format is invalid!")

        User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION,
                        data=self.json())

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }


    @classmethod
    def find_by_email(cls,email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)