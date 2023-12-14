from Backend.DAOs.incomingTransaction import IncomingTransactionDAO
from Backend.DAOs.stored_in import StoredInDAO
from Backend.DAOs.supplies import SuppliesDao
from Backend.DAOs.warehouse_dao import WarehouseDAO
from Backend.handler.validation import ValidResponse, InvalidResponse, ValidationResponse, ValidatableTransaction
from flask import jsonify


class IncomingTransactionHandler(ValidatableTransaction):
    def mapToDict(self, tup):
        my_dict = {}
        my_dict["itid"] = tup[0]
        my_dict["tdate"] = tup[1]
        my_dict["unit_buy_price"] = tup[2]
        my_dict["part_amount"] = tup[3]
        my_dict["sid"] = tup[4]
        my_dict["rid"] = tup[5]
        my_dict["tid"] = tup[6]
        my_dict["pid"] = tup[7]
        my_dict["uid"] = tup[8]
        my_dict["wid"] = tup[9]
        return my_dict


    def addIncomingTransaction(self, data):
        """
        Validates and adds a new incoming transaction.
        """
        response = self._validate_data(data)
        if response.isValid():
            transactionDate, partAmount, unitBuyPrice, partID, warehouseID, rackID, supplierID, userID = response.value
        else: return response.value

        response = self._validate_enough_supplier_stock(partID, supplierID, partAmount)
        if response.isValid(): stock = response.value
        else: return response.value

        cost = unitBuyPrice*partAmount
        response = self._validate_enough_budget_in_warehouse(unitBuyPrice, partAmount, warehouseID, cost)
        if not response.isValid(): return response.value

        response = self._validate_user_in_warehouse(userID, warehouseID)
        if not response.isValid(): return response.value

        response = self._validate_rack_exists(rackID)
        if response.isValid(): rack_capacity = response.value
        else: return response.value
        
        response = self._validate_rack_is_not_in_use_for_different_part(rackID, warehouseID, partID)
        if not response.isValid(): return response.value

        response = self._validate_amount_fits_in_rack(warehouseID, partID, rackID, rack_capacity, partAmount)
        if response.isValid(): current_amount_in_rack = response.value
        else: return response.value
        
        # Add transaction
        itid = IncomingTransactionDAO().addIncomingTransaction(unit_buy_price=unitBuyPrice,
                                                               sid=supplierID,
                                                               rid=rackID,
                                                               tdate=transactionDate,
                                                               part_amount=partAmount,
                                                               pid=partID,
                                                               uid=userID,
                                                               wid=warehouseID)
        if not itid: return jsonify(Error="Failed to add transaction"), 500

        # Update available stock
        supplies_DAO = SuppliesDao()
        count = supplies_DAO.decrease_stock(pid=partID, sid=supplierID, delta=partAmount)
        if not count: return jsonify(Error="Failed to update stock"), 500
        elif stock - partAmount == 0: supplies_DAO.delete_entry(pid=partID, sid=supplierID)

        # Update available budget
        new_budget = WarehouseDAO().decrease_budget(wid=warehouseID, delta=cost)
        if not new_budget: return jsonify(Error="Failed to update warehouse budget"), 500

        # Add to stored_in
        count = StoredInDAO().modify_quantity(wid=warehouseID,
                                              pid=partID,
                                              rid=rackID,
                                              new_quantity=current_amount_in_rack+partAmount)
        if not count:
            return jsonify(Error=
                f"Failed to modify quantity of part ({partID}) in warehouse ({warehouseID})"
                ), 500
        
        data["itid"] = itid
        return jsonify(Result=data), 201
    

    def getAllIncomingTransaction(self):
        """
        Returns all incoming transactions.
        """
        dao = IncomingTransactionDAO()
        dbtuples = dao.getAllIncomingTransaction()
        if dbtuples:
            result = []
            for tup in dbtuples:
                result.append(self.mapToDict(tup))
            return jsonify(Result=result)
        else:
            return jsonify(Error="Failed to load transactions"), 500


    def getIncomingTransactionById(self, itid):
        """
        Returns the incoming transaction with the given id.
        """
        dao = IncomingTransactionDAO()
        dbtuples = dao.getIncomingTransactionById(itid)
        if dbtuples:
            return jsonify(Result=self.mapToDict(dbtuples[0]))
        else:
            return jsonify(Error="Could not find matching incoming transaction"), 500
        

    def modifyIncomingTransactionByID(self, itid, data):
        """
        Modifies the given incoming transaction.
        Performs basic validation but does not update other tables.
        """
        response = self._validate_data(data)
        if response.isValid():
            transactionDate, partAmount, unitBuyPrice, partID, warehouseID, rackID, supplierID, userID = response.value
        else: return response.value

        response = self._validate_user_in_warehouse(userID, warehouseID)
        if not response.isValid(): return response.value

        response = self._validate_rack_exists(rackID)
        if not response.isValid(): return response.value
        
        response = self._validate_rack_is_not_in_use_for_different_part(rackID, warehouseID, partID)
        if not response.isValid(): return response.value

        dao = IncomingTransactionDAO()
        count = dao.modifyIncomingTransactionById(unit_buy_price=unitBuyPrice,
                                                 sid=supplierID,
                                                 rid=rackID,
                                                 tdate=transactionDate,
                                                 part_amount=partAmount,
                                                 pid=partID,
                                                 uid=userID,
                                                 wid=warehouseID,
                                                 itid=itid)
        if not count: return jsonify("Not Found"), 404
        return jsonify(data), 200

        


    def _validate_data(self, data) -> ValidationResponse:
        """
        Checks whether the data is valid.
        Returns the data if the response is valid.
        """
        try:
            transactionDate = data["transactionDate"]
            partAmount = data["partAmount"]
            unitBuyPrice = data["unitBuyPrice"]
            partID = data["partID"]
            warehouseID = data["warehouseID"]
            rackID = data["rackID"]
            supplierID = data["supplierID"]
            userID = data["userID"]
        except KeyError as e:
            return InvalidResponse(jsonify(Error={"Unexpected parameter names": e.args}), 400)
        # Verify nulls
        if not (transactionDate and partAmount and unitBuyPrice and partID
                and warehouseID and rackID and supplierID and userID):
            return InvalidResponse(jsonify(Error="Attributes cannot contain null fields."), 400)
        # Verify types
        for attr in (partID, warehouseID, rackID, supplierID, userID, partAmount):
            if not isinstance(attr, int):
                return InvalidResponse(jsonify(Error=f"Invalid attritube for type 'int' ({attr})"), 400)
        if not isinstance(unitBuyPrice, float) and not isinstance(unitBuyPrice, int):
            return InvalidResponse(jsonify(Error=f"Invalid type for unitBuyPrice ({unitBuyPrice})"), 400)
        if not isinstance(transactionDate, str):
            return InvalidResponse(jsonify(Error=f"Invalid type for transaction date ({transactionDate})"), 400)
        # Verify values are valid
        if unitBuyPrice < 0: return InvalidResponse(jsonify(Error="unitBuyPrice must be a positive number"), 400)
        if partAmount < 0: return InvalidResponse(jsonify(Error="partAmount must be a positive number"), 400)
        return ValidResponse(transactionDate, partAmount, unitBuyPrice, partID, warehouseID, rackID, supplierID, userID)