from Backend.DAOs.transaction import TransactionDAO
from flask import jsonify


class TransactionHandler:    
    def mapToDictWithType(self, tup):
        my_dict = {}
        my_dict["tid"] = tup[0]
        my_dict["tdate"] = tup[1]
        my_dict["part_amount"] = tup[2]
        my_dict["pid"] = tup[3]
        my_dict["uid"] = tup[4]
        my_dict["wid"] = tup[5]
        my_dict["type"] = tup[6]
        return my_dict


    def getAllTransactions(self):
        dao = TransactionDAO()
        dbtuples = dao.getAllTransactions()
        if dbtuples:
            result = []
            for tup in dbtuples:
                result.append(self.mapToDictWithType(tup))
            return jsonify(Result=result)
        else:
            return jsonify("Internal Server Error: Failed to load transactions"), 500
    

    def getTransactionById(self, tid):
        dao = TransactionDAO()
        dbtuples = dao.getTransactionByID(tid)
        if dbtuples:
            result = []
            for tup in dbtuples:
                result.append(self.mapToDictWithType(tup))
            return jsonify(Result=result)
        else:
            return jsonify("Failed to find matching transaction"), 404


    def getTransactionsByWarehouse(self, data):
        try:
            wid = data["wid"]
        except KeyError as e:
            return jsonify(Error={"Unexpected parameter names": e.args}), 400

        if wid is None:
            return jsonify(Error="Attributes cannot contain null fields."), 400
        
        if not isinstance(wid, int):
            return jsonify(Error="wid must be an integer"), 400

        dao = TransactionDAO()
        dbtuples = dao.getTransactionsByWarehouse(wid)
        if dbtuples:
            result = []
            for tup in dbtuples:
                result.append(self.mapToDictWithType(tup))
            return jsonify(Result=result)
        else:
            return jsonify(f"Failed to find transactions for warehouse {wid}"), 404
