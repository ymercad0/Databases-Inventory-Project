from Backend.DAOs.DAO import DAO


class PartDAO(DAO):
    def getAllParts(self):
        # object utilized to send queries to the DB and to iterate through the results from the query
        with self.conn.cursor() as cursor:
            res = []
            query = "SELECT pid, pname, pcolor, pmaterial, msrp FROM parts"
            cursor.execute(query)

            for row in cursor:
                res.append(row)  # adding the rows
            return res

    def searchByID(self, pid):
        with self.conn.cursor() as cursor:
            query = "SELECT pid, pname, pcolor, pmaterial, msrp FROM parts WHERE pid = %s"
            cursor.execute(query, (pid,))
            result = cursor.fetchone()
            return result

    def insertPart(self, name, color, material, msrp):
        with self.conn.cursor() as cursor:
            query = "INSERT INTO parts(pname, pcolor, pmaterial, msrp) VALUES (%s, %s, %s, %s) returning pid;"
            cursor.execute(query, (name, color, material, msrp))  # passing the args so it's more secure
            pid = cursor.fetchone()[0]
            self.conn.commit()  # to save the changes
            return pid

    def deleteByID(self, pid):
        with self.conn.cursor() as cursor:
            query = "DELETE FROM parts WHERE pid = %s"
            cursor.execute(query, (pid,))
            count = cursor.rowcount
            self.conn.commit()  # to save the changes
            return count

    def updateByID(self, pid, name, color, material, msrp):
        with self.conn.cursor() as cursor:
            query = "UPDATE parts set pname=%s, pcolor=%s, pmaterial=%s, msrp=%s where pid = %s;"
            cursor.execute(query, (name, color, material, msrp, pid,))  # passing the args so it's more secure
            count = cursor.rowcount
            self.conn.commit()  # to save the changes
            return count

    def inStock(self, pid):
        res = self._generic_retrieval_query(query="""
                                            SELECT COUNT(pid)
                                            FROM supplies
                                            WHERE pid = %s;
                                            """,
                                            substitutions=pid)
        if not res or len(res) == 0: return None
        return res[0][0]

    def inTransaction(self, pid):
        res = self._generic_retrieval_query(query="""
                                            SELECT COUNT(pid)
                                            FROM transactions
                                            WHERE pid = %s;
                                            """,
                                            substitutions=pid)
        if not res or len(res) == 0: return None
        return res[0][0]

    def beingStored(self, pid):
        res = self._generic_retrieval_query(query="""
                                            SELECT COUNT(pid)
                                            FROM stored_in
                                            WHERE pid = %s;
                                            """,
                                            substitutions=pid)
        if not res or len(res) == 0: return None
        return res[0][0]