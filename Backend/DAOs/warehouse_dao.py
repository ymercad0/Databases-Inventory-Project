from Backend.DAOs.DAO import DAO
import psycopg2


class WarehouseDAO(DAO):

    def name_city_combo_exists(self, wname, wcity):
        count = self._generic_retrieval_query(query="""
                                              SELECT COUNT(*)
                                              FROM warehouse
                                              WHERE wname = %s
                                              AND wcity = %s
                                              """,
                                              substitutions=(wname, wcity))
        if not count: return None
        return count[0][0] > 0

    def getAllWarehouses(self):
        """Execute a query to get all the warehouses from the Warehouses Table in the database.
        
        Return: all records from the Warehouses Table in the database.
        """
        return self._getAllEntries(table_name="warehouse",
                                   columns=("wid",
                                            "wname",
                                            "wcountry",
                                            "wregion",
                                            "wcity",
                                            "wstreet",
                                            "wzipcode",
                                            "wbudget"))

    def insertWarehouse(self, warehouse_name: str,
                        warehouse_country: str,
                        warehouse_region: str,
                        warehouse_city: str,
                        warehouse_street: str,
                        warehouse_zipcode: str,
                        warehouse_budget: float) -> int:
        """Insert a new warehouse in the Warehouses Table in the database.

        Args:
            warehouse_name (str): Name of the warehouse to be inserted.
            warehouse_country (str): Country of the warehouse to be inserted.
            warehouse_region (str): Region of the warehouse to be inserted.
            warehouse_city (str): City of the warehouse to be inserted.
            warehouse_street (str): Street of the warehouse to be inserted.
            warehouse_zipcode (str): Zipcode of the warehouse to be inserted.
            warehouse_budge (float): Budget of the warehouse to be inserted.

        Returns:
            int: ID of the warehouse that was inserted.
        """
        return self._addEntry(table_name="warehouse",
                              id_name="wid",
                              columns=["wname", "wcountry", "wregion", "wcity", "wstreet", "wzipcode", "wbudget"],
                              values=[warehouse_name,
                                      warehouse_country,
                                      warehouse_region,
                                      warehouse_city,
                                      warehouse_street,
                                      warehouse_zipcode,
                                      warehouse_budget])

    def getWarehouseByID(self, wid: int):
        """Execute a query to get a warehouse from the Warehouses Table in the database.
        
        Return: a record from the Warehouses Table in the database which matches the given wid.
        """
        return self._getEntryByID(table_name="warehouse", id_name="wid", id_value=str(wid),
                                  columns=("wid", "wname", "wcountry", "wregion", "wcity", "wstreet", "wzipcode",
                                           "wbudget"))

    def insertWarehouse(self, warehouse_name: str,
                        warehouse_country: str,
                        warehouse_region: str,
                        warehouse_city: str,
                        warehouse_street: str, warehouse_zipcode: str,
                        warehouse_budget: float) -> int:
        """Insert a new warehouse in the Warehouses Table in the database.

        Args:
            warehouse_name (str): Name of the warehouse to be inserted.
            warehouse_country (str): Country of the warehouse to be inserted.
            warehouse_region (str): Region of the warehouse to be inserted.
            warehouse_city (str): City of the warehouse to be inserted.
            warehouse_street (str): Street of the warehouse to be inserted.
            warehouse_zipcode (str): Zipcode of the warehouse to be inserted.
            warehouse_budge (float): Budget of the warehouse to be inserted.

        Returns:
            int: ID of the warehouse that was inserted.
        """
        return self._addEntry(table_name="warehouse",
                              id_name="wid",
                              columns=["wname", "wcountry", "wregion", "wcity", "wstreet", "wzipcode", "wbudget"],
                              values=[warehouse_name,
                                      warehouse_country,
                                      warehouse_region,
                                      warehouse_city,
                                      warehouse_street,
                                      warehouse_zipcode,
                                      warehouse_budget])

    def updateWarehouseByID(self, wid: int, warehouse_name: str,
                            warehouse_country: str,
                            warehouse_region: str,
                            warehouse_city: str,
                            warehouse_street: str, warehouse_zipcode: str,
                            warehouse_budget: float) -> object:
        return self._modifyEntryByID(table_name="warehouse",
                                     id_name="wid",
                                     id_value=str(wid),
                                     columns=["wname",
                                              "wcountry",
                                              "wregion",
                                              "wcity",
                                              "wstreet", "wzipcode", "wbudget"],
                                     values=[warehouse_name,
                                             warehouse_country,
                                             warehouse_region,
                                             warehouse_city,
                                             warehouse_street,
                                             warehouse_zipcode,
                                             warehouse_budget])

    def deleteWarehouseByID(self, wid: int) -> object:
        """Delete a warehouse from the Warehouses Table in the database by the given ID.

        Args:
            wid (int): ID of the warehouse to be deleted.

        Returns:
            object: ID of the warehouse that was deleted.
        """
        return self._deleteEntryByID(table_name="warehouse",
                                     id_name="wid",
                                     id_value=str(wid))

    def get_warehouse_budget(self, wid):
        result = self._generic_retrieval_query(query="""
                                               SELECT wbudget
                                               FROM warehouse
                                               WHERE wid = %s
                                               """,
                                               substitutions=wid)
        if not result or len(result) == 0: return None
        return result[0][0]

    def decrease_budget(self, wid, delta):
        """
        Decreases the budget by the given delta.
        Returns the new number of affected rows.

        WARNING: If delta is negative, will return None and not execute any operations.
        """
        if delta < 0: return None
        with self.conn.cursor() as cursor:
            query = "UPDATE warehouse SET wbudget = wbudget-%s WHERE wid = %s AND wbudget >= %s"
            try:
                cursor.execute(query, (delta, wid, delta))
                count = cursor.rowcount
                self.conn.commit()
                return count
            except psycopg2.errors.Error as e:
                print(f"\n\nError in file: {__file__}\n{e.pgerror}\n\n")
                return None

    def increase_budget(self, wid, delta):
        """
        Increases the budget by the given delta.
        Returns the new number of affected rows.

        WARNING: If delta is negative, will return None and not execute any operations.
        """
        if delta < 0: return None
        with self.conn.cursor() as cursor:
            # integer overflow who?
            query = "UPDATE warehouse SET wbudget = wbudget+%s WHERE wid = %s"
            try:
                cursor.execute(query, (delta, wid))
                count = cursor.rowcount
                self.conn.commit()
                return count
            except psycopg2.errors.Error as e:
                print(f"\n\nError in file: {__file__}\n{e.pgerror}\n\n")
                return None

    def warehouseInUsers(self,wid:int) -> bool:
        """Check if a warehouse is in the Users Table in the database.

        Args:
            wid (int): ID of the warehouse to be checked.

        Returns:
            bool: True if the warehouse is in the Users Table in the database, False otherwise.
        """

        result = self._generic_retrieval_query(query="""select count(wid) from users
                                             where wid = %s
                                             """, substitutions=wid)

        return True if result[0][0]==0 else False

    def warehouseInTransfer(self,to_warehouse:int) -> bool:
        """Check if a warehouse is in the Transfer Table in the database.

        Args:
            wid (int): ID of the warehouse to be checked.

        Returns:
            bool: True if the warehouse is in the Transfer Table in the database, False otherwise.
        """
        result = self._generic_retrieval_query(query="""
                                             select count(to_warehouse) from transfer
                                             where to_warehouse = %s
                                             """, substitutions=to_warehouse)
        return True if result[0][0]==0 else False

    def warehouseInTransactions(self,wid:int) -> bool:
        """Check if a warehouse is in the Transactions Table in the database.

        Args:
            wid (int): ID of the warehouse to be checked.

        Returns:
            bool: True if the warehouse is in the Transactions Table in the database, False otherwise.
        """
        result = self._generic_retrieval_query(query="""
                                             select count(wid) from transactions
                                             where wid = %s
                                             """, substitutions=wid)
        return True if result[0][0]==0 else False

    def warehouseInStoredIn(self,wid:int) -> bool:
        """Check if a warehouse has racks stored in it

        Args:
            wid (int): warehouse id of the warehouse to be checked

        Returns:
            bool: True if the warehouse is in the table, False otherwise
        """

        result = self._generic_retrieval_query(query="""
                                              select count (wid)
                                              from stored_in
                                              where wid = %s 
                                              """, substitutions=wid)
        return True if result[0][0]==0 else False

    def worksIn(self, wid: int, uid: int) -> bool:
        """Returns a bool indicating whether a user works in a warehouse or not."""
        query = """SELECT username  
                    FROM users
                    WHERE uid = %s AND wid = %s;"""

        res = self._generic_retrieval_query(query, substitutions=(uid, wid))
        return res is not None and res != []

    # For Global/Local statistics
    def get_top_racks(self):
        """Part of the global statistics. Gets the top 10 warehouses with the most racks."""
        query = """SELECT wname as warehouse, COUNT(rid) as rack_count
                    FROM warehouse NATURAL INNER JOIN stored_in
                    GROUP BY wname
                    ORDER BY rack_count DESC
                    LIMIT 10;"""
        return self._generic_retrieval_query(query)

    def get_most_exchanges(self):
        """Part of the global statistics. Gets the top 5 warehouses
        with the most exchanges/transfers."""
        query = """SELECT wname as warehouse, COUNT(*) as total_transfers
                    FROM warehouse
                    NATURAL INNER JOIN transactions
                    NATURAL INNER JOIN transfer
                    GROUP BY wname
                    ORDER BY total_transfers DESC
                    LIMIT 5;"""
        return self._generic_retrieval_query(query)

    def get_top_user_transactions(self):
        """Part of the global statistics. Gets the top 3 users that made the most transactions."""
        query = """SELECT ufname as first_name, ulname as last_name, COUNT(*) as transaction_count
                    FROM users
                    NATURAL INNER JOIN transactions
                    GROUP BY ufname, ulname
                    ORDER BY transaction_count DESC
                    LIMIT 3;"""
        return self._generic_retrieval_query(query)

    def get_least_outgoing(self):
        """Part of the global statistics. Gets the top 3 warehouses
        with the least outgoing transactions."""
        query = """SELECT wname as warehouse, COUNT(otid) as total_outgoing_transactions
                    FROM warehouse
                    NATURAL INNER JOIN transactions
                    NATURAL INNER JOIN outgoing_transaction
                    GROUP BY wname
                    ORDER BY total_outgoing_transactions ASC
                    LIMIT 3;"""
        return self._generic_retrieval_query(query)

    def get_most_incoming(self):
        """Part of the global statistics. Top 5 warehouses with the most incoming transactions."""
        query = """SELECT wname as warehouse, COUNT(*) as total_incoming_transactions
                    FROM warehouse
                    NATURAL INNER JOIN transactions
                    NATURAL INNER JOIN incoming_transaction
                    GROUP BY wname
                    ORDER BY total_incoming_transactions DESC
                    LIMIT 5;"""
        return self._generic_retrieval_query(query)

    def get_most_city(self):
        """Part of the global statistics. Top 3 warehouse cities with the most transactions."""
        query = """SELECT wcity as warehouse_city, COUNT(*) as total_transactions
                    FROM warehouse
                    NATURAL INNER JOIN transactions
                    GROUP BY wcity
                    ORDER BY total_transactions DESC
                    LIMIT 3;
                    """
        return self._generic_retrieval_query(query)

    def get_profit_yearly(self, wid: int):
        """Part of the local statistics. Returns specified warehouse's profit by year."""
        query = """WITH net_expenses AS (
                    SELECT t.tid,
                    COALESCE(SUM(ot.unit_sale_price * t.part_amount), 0) AS total_earnings,
                    COALESCE(SUM(it.unit_buy_price * t.part_amount), 0) AS total_costs
                    FROM transactions as t
                    LEFT JOIN outgoing_transaction as ot ON t.tid = ot.tid
                    LEFT JOIN incoming_transaction as it ON t.tid = it.tid
                    GROUP BY t.tid
                )
                
                SELECT EXTRACT(YEAR FROM tdate) AS year,
                wname AS warehouse,
                SUM(ne.total_earnings - ne.total_costs) AS net_profit
                FROM warehouse
                NATURAL INNER JOIN transactions
                NATURAL INNER JOIN net_expenses as ne
                WHERE wid = %s
                GROUP BY year, wname
                ORDER BY year DESC;"""
        return self._generic_retrieval_query(query, substitutions=wid)

    def get_bottom_racks(self, wid: int):
        """Part of the local statistics. Returns bottom 3 racks by material/type in a warehouse."""
        query = """WITH part_types AS (
                    SELECT pname AS part, pmaterial AS type, COUNT(*) AS part_count
                    FROM stored_in
                    NATURAL INNER JOIN parts
                    WHERE wid = %s
                    GROUP BY pname, pmaterial
                )
                
                SELECT part, type, part_count
                FROM part_types
                ORDER BY part_count ASC
                LIMIT 3;"""
        return self._generic_retrieval_query(query, substitutions=wid)

    def get_most_user_exchanges(self, wid: int):
        """Part of the local statistics. Returns top 3 users that received the most
        exchanges from a warehouse."""
        query = """WITH user_exchanges as (
                    SELECT ufname as first_name, ulname as last_name, COUNT(*) AS transfer_count
                    FROM users as u
                    INNER JOIN transfer as tr ON u.uid = tr.user_requester
                    WHERE wid=%s
                    GROUP BY first_name, last_name
                )
                
                SELECT * FROM user_exchanges
                ORDER BY transfer_count DESC
                LIMIT 3;"""
        return self._generic_retrieval_query(query, substitutions=wid)

    def get_most_expensive_racks(self, wid: int):
        """Part of the local statistics. Top 5 most expensive racks in the warehouse."""
        query = """SELECT wname as warehouse, rname as rack, SUM(msrp*parts_qty) as rack_price
                    FROM warehouse
                    NATURAL INNER JOIN stored_in
                    NATURAL INNER JOIN racks
                    NATURAL INNER JOIN parts
                    WHERE wid = %s
                    GROUP BY wname, rname
                    ORDER BY rack_price DESC
                    LIMIT 5;"""
        return self._generic_retrieval_query(query, substitutions=wid)

    def get_least_daily_cost(self, wid: int):
        """Part of the local statistics. Top 3 days with the smallest incoming transactions’ cost."""
        query = """WITH daily_costs AS (
                        SELECT tdate as transaction_date,
                        SUM(unit_buy_price * part_amount) AS total_incoming_cost
                        FROM transactions
                        NATURAL INNER JOIN incoming_transaction
                        WHERE wid = %s
                        GROUP BY tdate
                        )

                    SELECT *
                    FROM daily_costs
                    ORDER BY total_incoming_cost ASC
                    LIMIT 3;"""
        return self._generic_retrieval_query(query, substitutions=wid)

    def get_least_rack_stock(self, wid: int):
        """Part of the local statistics. Top 5 racks with quantity under the 25% capacity threshold."""
        query = """
                SELECT rname as rack, rcapacity * 0.25 AS low_capacity, parts_qty
                FROM racks
                NATURAL INNER JOIN stored_in
                NATURAL INNER JOIN parts
                WHERE rid IN (SELECT rid FROM stored_in WHERE wid = %s)
                AND parts_qty < rcapacity * 0.25
                ORDER BY parts_qty DESC
                LIMIT 5;
                """
        return self._generic_retrieval_query(query, substitutions=wid)

    def get_most_suppliers(self, wid: int):
        """Part of the local statistics. Top 3 suppliers that supplied to the given warehouse."""
        query = """
                WITH suppliers AS (
                    SELECT sname AS supplier_name, COUNT(wid) AS supply_count
                    from incoming_transaction
                    natural  inner join transactions
                    natural inner join warehouse
                    natural inner join supplier
                    WHERE wid = %s
                    GROUP BY sname
                    )
                SELECT * FROM suppliers
                ORDER BY supply_count DESC
                LIMIT 3;
                """
        return self._generic_retrieval_query(query, substitutions=(wid,))
    
    def getAllWarehouseParts(self,wid:int):
        query = """
        select pid,pname,pcolor,pmaterial,msrp,parts_qty
        from stored_in natural inner join parts
        where wid = %s """
        return self._generic_retrieval_query(query, substitutions=(wid,))
