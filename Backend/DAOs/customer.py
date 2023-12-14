from Backend.DAOs.DAO import DAO


class CustomerDAO(DAO):
    def getAllCustomers(self):
        return self._getAllEntries(table_name="customer",
                                   columns=("cid", "cfname", "clname", "czipcode", "cphone"))

    def searchByPhone(self, cphone, cid=None):
        with self.conn.cursor() as cur:
            if cid:
                query = """SELECT cid FROM customer WHERE cphone = %s and cid != %s;"""
                cur.execute(query, (cphone,cid))
            else:
                query = """SELECT cid FROM customer WHERE cphone = %s;"""
                cur.execute(query, (cphone,))
            res = cur.fetchone()
            return res

    def getCustomerById(self, cid):
        return self._getEntryByID(table_name="customer",
                                  id_name="cid",
                                  id_value=cid,
                                  columns=("cid", "cfname", "clname", "czipcode", "cphone"))

    def addCustomer(self, cfname, clname, czipcode, cphone):
        return self._addEntry(table_name="customer",
                              id_name="cid",
                              columns=("cfname", "clname", "czipcode", "cphone"),
                              values=(cfname, clname, czipcode, cphone))

    def modifyCustomerById(self, cfname, clname, czipcode, cphone, cid):
        return self._modifyEntryByID(table_name="customer",
                                     id_name="cid",
                                     id_value=cid,
                                     columns=("cfname", "clname", "czipcode", "cphone"),
                                     values=(cfname, clname, czipcode, cphone))

    def deleteCustomerById(self, cid):
        return self._deleteEntryByID(table_name="customer",
                                     id_name="cid",
                                     id_value=cid)