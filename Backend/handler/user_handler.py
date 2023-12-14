from flask import jsonify
from Backend.DAOs.user_dao import UserDAO
from Backend.DAOs.warehouse_dao import WarehouseDAO


class UserHandler:
    """
    UserHandler takes care of processing all the data
    from the user and transforming it into a JSON
    to be sent to the database in order to be processed.
    The handler also takes care of connecting to the DB
    and extract lists of users.
    """

    def __init__(self):
        # Capture in an object the query to be sent to the DB.
        self.userDAO = UserDAO()
        self.warehouseDAO = WarehouseDAO()

    def build_user_dict(self, row: tuple) -> dict:
        """Builds dictionary that contains
        all the information from a user.

        Args:
            row (tuple): A record, given as a tuple, from the
        Users table in the database.

        Returns:
            dict: A dictionary that contains all the information mapped to
        the correct keys. This is so that later the dictionary can be
        transformed into JSON format.
        """
        user_dict = {}
        user_dict['uid'] = row[0]
        user_dict['ufname'] = row[1]
        user_dict['ulname'] = row[2]
        user_dict['username'] = row[3]
        user_dict['uemail'] = row[4]
        user_dict['upassword'] = row[5]
        user_dict['wid'] = row[6]

        return user_dict

    def getAllUsers(self) -> object:
        """Returns all users from the Users Table in the database.

        Return: JSON object that contains all the users from the Users Table that were found in the database.
        """

        all_users_tuples = self.userDAO.getAllUsers()
        all_users_result = []
        for record in all_users_tuples:
            all_users_result.append(self.build_user_dict(record))
        return jsonify(Users=all_users_result)

    @staticmethod
    def username_exists(username, uid=None, dao=UserDAO()):
        # Can't insert/update a user with an existing username
        existing_uname = dao.searchUserByUsername(username, uid=uid) is not None
        if existing_uname:
            return {"Error": f"Error: The username '{username}' already exists!"}

        return {}

    @staticmethod
    def user_email_exists(uemail, uid=None, dao=UserDAO()):
        # Can't insert/update a user with an existing username
        existing_uemail = dao.searchUserByEmail(uemail, uid=uid) is not None
        if existing_uemail:
            return {"Error": f"Error: The email '{uemail}' already exists!"}
        return {}

    def getUserByID(self, uid: int) -> object:
        """ Return a record, or series of records that correspond to the user with the given uid.

        Args:
            uid (int): The uid of the user to be searched.

        Returns:
            object: JSON object that contains all the data found of the user with the given uid.
        """

        uid_row = self.userDAO.getUserByID(uid)
        # If the user was not found, return a 404 error.
        if not uid_row:
            return jsonify(Error="User Not Found. Input an ID of a user that exists"), 404
        return jsonify(User=self.build_user_dict(uid_row[0]))

    def insertUser(self, data: object) -> object:
        """Insert a user with the given data in the users table

        Args:
            data (object): JSON object containing information
            to create a user.

        Returns:
            object: JSON object that contains the ID of the user that was inserted.
        """
        if len(data) != 6:
            return jsonify(
                Error="Incorrect amount of data has been sent. The required fields are: ufname,ulnane,username,email and wid "), 400
        try:
            ufname = data['ufname']
            ulname = data['ulname']
            username = data['username']
            uemail = data['uemail']
            upassword = data['upassword']
            wid = data['wid']
        except KeyError:
            return jsonify(
                Error="Unexpected or Incorrect attribute in post request. Check that the fields of the request are correct"), 400

        # Check that the data is not empty.
        for key in data:
            if not data[key]:
                return jsonify(Error='Missing ' + key + ' attribute'), 400

        # Check that the all fields except wid are strings.
        for key in data:
            if key != 'wid' and not isinstance(data[key], str):
                return jsonify(Error=f'{key} has to be a string.'), 400

        # Check that the warehouse ID is an integer.
        if not isinstance(wid, int):
            return jsonify(Error='wid has to be an integer.'), 400
        # Check that the warehouse ID is a positive integer.
        elif wid <= 0:
            return jsonify(Error='wid has to be a positive integer greater than zero.'), 400
        # Check that the warehouse exists.
        elif not self.warehouseDAO.getWarehouseByID(wid):
            return jsonify(Error="User can not belong to a Warehouses that does not exist"), 404
        # Data has been verified  up to this point. It is safe to insert it in the DB
        else:
            username_exists = self.username_exists(username, dao=self.userDAO).get("Error")
            if username_exists: return jsonify(username_exists), 404
            email_exists = self.user_email_exists(uemail, dao=self.userDAO).get("Error")
            if email_exists: return jsonify(email_exists), 404
            uid = self.userDAO.insertUser(ufname, ulname, username, uemail, upassword, wid)
            inserted_user = {}
            inserted_user['uid'] = uid
            inserted_user['ufname'] = ufname
            inserted_user['ulname'] = ulname
            inserted_user['username'] = username
            inserted_user['uemail'] = uemail
            inserted_user['upassword'] = upassword
            inserted_user['wid'] = wid
            return jsonify(User=inserted_user), 201

    def updateUserByID(self, uid: int, data: object) -> object:
        try:
            ufname = data['ufname']
            ulname = data['ulname']
            username = data['username']
            uemail = data['uemail']
            upassword = data['upassword']
            wid = data['wid']
        except KeyError:
            return jsonify(Error="Unexpected attributes in post request"), 400

        # Check that the data is not empty.
        for key in data:
            if not data[key]:
                return jsonify(Error='Missing ' + key + ' attribute'), 400

        for key in data:
            if key != 'wid' and not isinstance(data[key], str):
                return jsonify(Error=f'{key} has to be a string.'), 400

        # Check that the user ID is an integer.
        if not isinstance(uid, int):
            return jsonify(Error='wid has to be an integer.'), 400
        # Check that the user ID is a positive integer.
        elif uid <= 0:
            return jsonify(Error='wid has to be a positive integer greater than zero.'), 400

        # Check that the user exists
        elif not self.userDAO.getUserByID(uid):
            return jsonify(Error="User does not exist"), 404
        # Check that the warehouse ID is an integer.
        elif not isinstance(wid, int):
            return jsonify(Error='wid has to be an integer.'), 400
        # Check that the warehouse ID is a positive integer.
        elif wid <= 0:
            return jsonify(Error='wid has to be a positive integer greater than zero.'), 400
        # Check that the warehouse exists.
        elif not self.warehouseDAO.getWarehouseByID(wid):
            return jsonify(Error="User can not belong to a Warehouses that does not exist"), 404
        else:
            username_exists = self.username_exists(username, uid=uid, dao=self.userDAO).get("Error")
            if username_exists: return jsonify(username_exists), 404
            email_exists = self.user_email_exists(uemail, uid=uid, dao=self.userDAO).get("Error")
            if email_exists: return jsonify(email_exists), 404
            self.userDAO.updateUserByID(uid, ufname, ulname, username, uemail, upassword, wid)
            return jsonify(f"Updated user with id: {uid}"), 200

    def deleteUserByID(self, uid: int) -> object:
        """Delete a user from the Users table with the given uid.

        Args:
            uid (int): ID of the user to be deleted.

        Returns:
            object: JSON object that contains the ID of the deleted user.
        """
        if not uid:
            return jsonify(Error="uid was not given."), 400

        elif type(uid) != int:
            return jsonify(Error="uid has to be of type integer.")

        elif uid <= 0:
            return jsonify(Error="uid has to be a positive number greater than zero.")

        elif not self.userDAO.getUserByID(uid):
            return jsonify(Error="User not found"), 404
        #  Can not delete a user that is referenced in a Transaction.
        elif not self.userDAO.userHasTransactions(uid):
            return jsonify(Error="Can not delete a user that is referenced in a Transaction"), 400
        elif not self.userDAO.userHasTransfers(uid):
            return jsonify(Error="Can not delete a user that is referenced in a Transfer"), 400
        else:
            self.userDAO.deleteUserByID(uid)
            return jsonify(f'Deleted user with id: {uid}'), 200
        
    
