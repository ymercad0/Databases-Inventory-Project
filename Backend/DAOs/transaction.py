from Backend.DAOs.DAO import DAO

class TransactionDAO(DAO):
    def getAllTransactions(self):
        return self._generic_retrieval_query(query="""
                                            SELECT transactions.tid, tdate, part_amount, pid, uid, wid,
                                                CASE
                                                    WHEN incoming_transaction.tid IS NOT NULL THEN 'INCOMING'
                                                    WHEN outgoing_transaction.tid IS NOT NULL THEN 'OUTGOING'
                                                    WHEN transfer.tid IS NOT NULL THEN 'TRANSFER'
                                                    ELSE 'NOT FOUND'
                                                END AS type
                                            FROM transactions
                                            LEFT OUTER JOIN transfer ON transactions.tid = transfer.tid
                                            LEFT OUTER JOIN incoming_transaction ON transactions.tid = incoming_transaction.tid
                                            LEFT OUTER JOIN outgoing_transaction ON transactions.tid = outgoing_transaction.tid
                                            ORDER BY tdate DESC
                                             """)
 
    def getTransactionByID(self, tid):
        return self._generic_retrieval_query(query="""
                                            SELECT transactions.tid, tdate, part_amount, pid, uid, wid,
                                                CASE
                                                    WHEN incoming_transaction.tid IS NOT NULL THEN 'INCOMING'
                                                    WHEN outgoing_transaction.tid IS NOT NULL THEN 'OUTGOING'
                                                    WHEN transfer.tid IS NOT NULL THEN 'TRANSFER'
                                                    ELSE 'NOT FOUND'
                                                END AS type
                                            FROM transactions
                                            LEFT OUTER JOIN transfer ON transactions.tid = transfer.tid
                                            LEFT OUTER JOIN incoming_transaction ON transactions.tid = incoming_transaction.tid
                                            LEFT OUTER JOIN outgoing_transaction ON transactions.tid = outgoing_transaction.tid
                                            WHERE transactions.tid = %s
                                            ORDER BY tdate DESC
                                             """,
                                             substitutions=(tid))
    
    def getTransactionsByWarehouse(self, wid):
        return self._generic_retrieval_query(query="""
                                            SELECT transactions.tid, tdate, part_amount, pid, uid, wid,
                                                CASE
                                                    WHEN incoming_transaction.tid IS NOT NULL THEN 'INCOMING'
                                                    WHEN outgoing_transaction.tid IS NOT NULL THEN 'OUTGOING'
                                                    WHEN transfer.tid IS NOT NULL THEN 'TRANSFER'
                                                    ELSE 'NOT FOUND'
                                                END AS type
                                            FROM transactions
                                            LEFT OUTER JOIN transfer ON transactions.tid = transfer.tid
                                            LEFT OUTER JOIN incoming_transaction ON transactions.tid = incoming_transaction.tid
                                            LEFT OUTER JOIN outgoing_transaction ON transactions.tid = outgoing_transaction.tid
                                            WHERE transactions.wid = %s
                                            OR transfer.to_warehouse = %s
                                            ORDER BY tdate DESC
                                             """,
                                             substitutions=(wid, wid))