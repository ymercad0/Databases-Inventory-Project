from Backend.DAOs.DAO import DAO

class OutgoingTransactionDAO(DAO):
    def getAllOutgoingTransaction(self):
        return self._generic_retrieval_query(
            """
            SELECT otid, tdate, unit_sale_price, part_amount, cid, tid, pid, uid, wid
            FROM outgoing_transaction
            NATURAL INNER JOIN transactions;
            """
        )
    

    def getOutgoingTransactionById(self, otid):
        return self._generic_retrieval_query(
            query="""
            SELECT otid, tdate, unit_sale_price, part_amount, cid, tid, pid, uid, wid
            FROM outgoing_transaction
            NATURAL INNER JOIN transactions
            WHERE otid = %s;
            """,
            substitutions=(otid)
        )


    def addOutgoingTransaction(self, unit_sale_price, cid, tdate, part_amount, pid, uid, wid):
        tid = self._addEntry(table_name="transactions",
                             id_name="tid",
                             columns=("tdate", "part_amount", "pid", "uid", "wid"),
                             values=(tdate, part_amount, pid, uid, wid))
        otid = self._addEntry(table_name="outgoing_transaction",
                              id_name="otid",
                              columns=("unit_sale_price", "cid", "tid"),
                              values=(unit_sale_price, cid, tid))
        return otid


    def modifyOutgoingTransactionById(self, unit_sale_price, cid, tdate, part_amount, pid, uid, wid, otid):
        result = self._generic_retrieval_query(
            query="""
            SELECT tid
            FROM transactions
            NATURAL INNER JOIN outgoing_transaction
            WHERE otid = %s;
            """,
            substitutions=otid
        )
        if not result: return None
        tid = result[0]
        rowcountTransactions = self._modifyEntryByID(table_name="transactions",
                                                     id_name="tid",
                                                     id_value=tid,
                                                     columns=("tdate", "part_amount", "pid", "uid", "wid"),
                                                     values=(tdate, part_amount, pid, uid, wid))
        if not rowcountTransactions:
            return None
        rowcountOutgoingTransactions = self._modifyEntryByID(table_name="outgoing_transaction",
                                     id_name="tid",
                                     id_value=tid,
                                     columns=("unit_sale_price", "cid"),
                                     values=(unit_sale_price, cid))
        return rowcountOutgoingTransactions