from Backend.DAOs.DAO import DAO
import psycopg2


class RackDAO(DAO):
    def getAllRacks(self):
        with self.conn.cursor() as cur:
            res = []
            query = "select rid, rname, rcapacity from racks"
            cur.execute(query)

            for row in cur:
                res.append(row)
            return res

    def addRack(self, rname, rcapacity):
        with self.conn.cursor() as cur:
            query = "INSERT INTO racks(rname, rcapacity) VALUES (%s, %s) returning rid;"
            try:
                cur.execute(query, (rname, rcapacity))
            except psycopg2.errors.Error as e:
                print(f"\n\nError in file: {__file__}\n{e.pgerror}\n\n")
                return None
            rid = cur.fetchone()[0]
            self.conn.commit()
            return rid

    def getRackById(self, rid):
        with self.conn.cursor() as cursor:
            query = "select rid, rname, rcapacity from racks where rid = %s;"
            cursor.execute(query, (rid,))

            res = cursor.fetchone()
            print("res:", res)
            return res

    def modifyRackById(self, rid, rname, rcapacity):
        with self.conn.cursor() as cursor:
            query = "UPDATE racks SET rname = %s, rcapacity = %s WHERE rid = %s;"
            cursor.execute(query, (rname, rcapacity, rid))
            count = cursor.rowcount
            print(count)
            self.conn.commit()
            return count

    def deleteRackById(self, rid):
        with self.conn.cursor() as cursor:
            query = "DELETE FROM racks WHERE rid = %s"
            cursor.execute(query, (rid,))
            count = cursor.rowcount
            self.conn.commit()
            return count
    
    def get_capacity(self, rid):
        result = self._generic_retrieval_query(query="""
                                               SELECT rcapacity
                                               FROM racks
                                               WHERE rid = %s
                                               """,
                                               substitutions=rid)
        if not result: return None
        return result[0][0]

    def stores_parts(self, rid):
        res = self._generic_retrieval_query(query="""
                                            SELECT pid
                                            FROM stored_in
                                            WHERE rid = %s
                                            """,
                                            substitutions=rid)
        if not res:
            return 0
        return res[0][0]

    def in_incoming_transaction(self, rid):
        res = self._generic_retrieval_query(query="""
                                            SELECT itid
                                            FROM incoming_transaction
                                            WHERE rid = %s
                                            """,
                                            substitutions=rid)
        if not res:
            return 0
        return res[0][0]

    def name_exists(self, name):
        res = self._generic_retrieval_query(query="""
                                            SELECT COUNT(rid)
                                            FROM racks
                                            WHERE rname = %s;
                                            """,
                                            substitutions=(name,))
        if not res: return 0
        return res[0][0]
