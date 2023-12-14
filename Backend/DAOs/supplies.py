from Backend.DAOs.DAO import DAO
import psycopg2

class SuppliesDao(DAO):
    def get_stock_for_part_and_supplier(self, pid, sid):
        """
        Gets the stock for the given part and supplier
        or None if the entry doesn't exist or the query fails.
        """
        stock = self._generic_retrieval_query(query="""
                                              SELECT stock
                                              FROM supplies
                                              WHERE pid = %s
                                              AND sid = %s
                                              """,
                                              substitutions=(pid, sid))
        if not stock or len(stock) == 0: return None
        return stock[0][0]
    

    def decrease_stock(self, pid, sid, delta):
        """
        Decreases the stock by the given delta.
        Returns the new number of affected rows.

        WARNING: If delta is negative or 0, will return None and not execute any operations.
        """
        if delta <= 0: return None
        with self.conn.cursor() as cursor:
            query = "UPDATE supplies SET stock = stock-%s WHERE pid = %s AND sid = %s AND stock >= %s"
            try:
                cursor.execute(query, (delta, pid, sid, delta))
                count = cursor.rowcount
                self.conn.commit()
                return count
            except psycopg2.errors.Error as e:
                print(f"\n\nError in file: {__file__}\n{e.pgerror}\n\n")
                return None 


    def delete_entry(self, pid, sid):
        """
        Deletes entires with the given pid and sid, if it exists, and return the number of affected rows.
        Otherwise, return None.
        """
        with self.conn.cursor() as cursor:
            query = "DELETE FROM supplies WHERE pid = %s AND sid = %s"
            try:
                cursor.execute(query, (pid, sid))
                count = cursor.rowcount
                self.conn.commit()
                return count
            except psycopg2.errors.Error as e:
                print(f"\n\nError in file: {__file__}\n{e.pgerror}\n\n")
                return None

    def get_parts_supplied(self, sid):
        query = """
        SELECT pid, pname, pcolor, pmaterial, msrp, sid, stock
        FROM parts NATURAL INNER JOIN supplies
        WHERE sid = %s"""
        return self._generic_retrieval_query(query, substitutions=sid)
