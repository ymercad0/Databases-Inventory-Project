from Backend.DAOs.DAO import DAO


class SupplierDAO(DAO):
    def getAllSuppliers(self):
        with self.conn.cursor() as cur:
            res = []
            query = "select sid, sname, scountry, scity, sstreet, szipcode, sphone from supplier"
            cur.execute(query)

            for row in cur:
                res.append(row)
            return res

    def insertSupplier(self, name, country, city, street, zipcode, phone):
        with self.conn.cursor() as cur:
            query = "INSERT INTO supplier(sname, scountry, scity, sstreet, szipcode, sphone) VALUES (%s, %s, %s, %s, %s, " \
                    "%s) returning sid; "
            cur.execute(query, (name, country, city, street, zipcode, phone))
            sid = cur.fetchone()[0]
            self.conn.commit()
            return sid

    def searchByID(self, sid):
        with self.conn.cursor() as cur:
            query = "SELECT sid, sname, scountry, scity, sstreet, szipcode, sphone FROM supplier WHERE sid = %s;"
            cur.execute(query, (sid,))
            res = cur.fetchone()
            return res

    def searchByName(self, sname, sid=None):
        with self.conn.cursor() as cur:
            if sid: #means we're updating, have to check that the previous name gets ignored (so it doesn't throw an error
                    # if not changed
                query = """SELECT sid FROM supplier WHERE sname = %s and sid != %s;"""
                cur.execute(query, (sname,sid))
            else: # only adding
                query = """SELECT sid FROM supplier WHERE sname = %s;"""
                cur.execute(query, (sname,))
            res = cur.fetchone()
        return res

    def searchByPhone(self, sphone, sid=None):
        with self.conn.cursor() as cur:
            if sid:
                query = """SELECT sid FROM supplier WHERE sphone = %s and sid != %s;"""
                cur.execute(query, (sphone, sid))
            else:
                query = """SELECT sid FROM supplier WHERE sphone = %s;"""
                cur.execute(query, (sphone,))
            res = cur.fetchone()
            return res

    def deleteByID(self, sid):
        with self.conn.cursor() as cur:
            query = "DELETE FROM supplier WHERE sid = %s"

            cur.execute(query, (sid,))
            count = cur.rowcount
            self.conn.commit()
            return count

    def updateByID(self, sid, name, country, city, street, zipcode, phone):
        with self.conn.cursor() as cur:
            query = "UPDATE supplier SET sname = %s, scountry = %s, scity = %s, sstreet = %s, szipcode = %s, sphone = %s " \
                    "WHERE sid = %s; "
            cur.execute(query, (name, country, city, street, zipcode, phone, sid,))
            count = cur.rowcount
            self.conn.commit()
            return count

    def suppliesParts(self, sid):
        res = self._generic_retrieval_query(query="""
                                                              SELECT COUNT(sid)
                                                              FROM supplies
                                                              WHERE sid = %s
                                                              """,
                                            substitutions=sid)
        if not res or len(res) == 0: return None
        return res[0][0]

    def inTransaction(self, sid):
        res = self._generic_retrieval_query(query="""
                                                      SELECT COUNT(sid)
                                                      FROM incoming_transaction
                                                      WHERE sid = %s
                                                      """,
                                            substitutions=sid)
        if not res or len(res) == 0: return None
        return res[0][0]
