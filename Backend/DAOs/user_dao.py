from Backend.DAOs.DAO import DAO
from typing import Iterable


class UserDAO(DAO):

    def getAllUsers(self) -> list:
        """Execute a query to get all the users from the Users Table in the database.

        Return: all records from the Users Table in the database.
        """
        return self._getAllEntries(table_name="users",
                                   columns=["uid", "ufname", "ulname", "username", "uemail", "upassword", "wid"])

    def getUserByID(self, uid: int) -> list:
        """Execute a query to get a user from the Users Table in the database.

        Return: a record from the Users Table in the database which matches the given uid.
        """
        return self._getEntryByID(table_name="users", id_name="uid", id_value=str(uid),
                                  columns=["uid", "ufname", "ulname", "username", "uemail", "upassword", "wid"])

    def searchUserByUsername(self, username: str, uid=None) -> Iterable | None:
        with self.conn.cursor() as cur:
            if uid:
                query = """SELECT uid FROM users WHERE username = %s and uid != %s;"""
                cur.execute(query, (username,uid))
            else:
                query = """SELECT uid FROM users WHERE username = %s;"""
                cur.execute(query, (username,))
            res = cur.fetchone()
            return res

    def searchUserByEmail(self, uemail: str, uid=None) -> Iterable | None:
        with self.conn.cursor() as cur:
            if uid:
                query = """SELECT uid FROM users WHERE uemail = %s and uid != %s;"""
                cur.execute(query, (uemail,uid))
            else:
                query = """SELECT uid FROM users WHERE uemail = %s;"""
                cur.execute(query, (uemail,))
            res = cur.fetchone()
            return res

    def insertUser(self, ufname: str, ulname: str, username: str, uemail: str, upassword: str, wid: int) -> int:
        """Insert a new user in the Users Table in the database.

        Args:
            ufname (str): First name of the user to be inserted.
            ulname (str): Last name of the user to be inserted.
            username (str): username of the user to be inserted.
            uemail (str): email of the user to be inserted.
            upassword (str): password of the user to be inserted.
            wid (int): ID of the warehouse the user is assigned to.

        Returns:
            int: ID of the user that was inserted.
        """
        return self._addEntry(table_name="users",
                              id_name="uid",
                              columns=["ufname", "ulname", "username", "uemail", "upassword", "wid"],
                              values=(ufname, ulname, username, uemail, upassword, wid))

    def updateUserByID(self, uid: int, ufname: str, ulname: str, username: str, uemail: str,
                       upassword: str, wid: int) -> int:
        """Update a user in the Users Table in the database by the given ID.

        Args:
            uid (int): ID of the user to be updated.
            ufname (str): Fist name of the user to be updated.
            ulname (str): Last name of the user to be updated.
            username (str): username of the user to be updated.
            uemail (str): email of the user to be updated.
            upassword (str): password of the user to be updated.
            wid (int): ID of the warehouse the user is assigned to.

        Returns:
            int: _description_
        """
        return self._modifyEntryByID(table_name="users",
                                     id_name="uid",
                                     id_value=str(uid),
                                     columns=["ufname", "ulname", "username", "uemail", "upassword", "wid"],
                                     values=(ufname, ulname, username, uemail, upassword, wid))

    def deleteUserByID(self, uid: int) -> int:
        """Delete a user from the Users Table in the database by the given ID

        Args:
            uid (int): ID of the user to be deleted.

        Returns:
            int: ID of the user that was deleted.
        """
        return self._deleteEntryByID(table_name="users",
                                     id_name="uid",
                                     id_value=str(uid))

    def userHasTransactions(self, uid: int) -> bool:
        """Check if a user has any transactions in the Transactions Table in the database.

        Args:
            uid (int): ID of the user to check.

        Returns:
            bool: True if the user has transactions, False otherwise.
        """
        result = self._generic_retrieval_query(query="""
                                              select count(uid) from transactions
                                              where uid = %s;
                                              """,
                                               substitutions=(uid,))
        return True if result[0][0] == 0 else False

    def userHasTransfers(self, user_requester: int) -> bool:
        """Check if a user has any transfers in the Transfer Table in the database.

        Args:
            uid (int): ID of the user to check.

        Returns:
            bool: True if the user has transfers, False otherwise.
        """
        result = self._generic_retrieval_query(query="""
                                                     select count(user_requester) from transfer
                                                     where user_requester = %s;
                                                     """, substitutions=(user_requester,))
        return True if result[0][0] == 0 else False
