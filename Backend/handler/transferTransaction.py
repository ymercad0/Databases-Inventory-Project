from Backend.DAOs.transferTransaction import TransferTransactionDAO
from Backend.DAOs.warehouse_dao import WarehouseDAO
from Backend.DAOs.parts import PartDAO
from Backend.DAOs.user_dao import UserDAO
from Backend.DAOs.stored_in import StoredInDAO
from Backend.DAOs.racks import RackDAO
from Backend.handler.validation import ValidResponse, InvalidResponse, ValidationResponse, ValidatableTransaction
from flask import jsonify


class TransferTransactionHandler(ValidatableTransaction):
    def __init__(self):
        self.transferTransactionDAO = TransferTransactionDAO()
        self.warehouse_dao = WarehouseDAO()
        self.user_dao = UserDAO()
        self.part_dao = PartDAO()
        self.stored_in_dao = StoredInDAO()
        self.rack_dao = RackDAO()
    
    def mapToDict(self, tup):
        my_dict = {}
        my_dict["transferID"] = tup[0]
        my_dict["transactionDate"] = tup[1]
        my_dict["partAmount"] = tup[2]
        my_dict["toWarehouse"] = tup[3]
        my_dict["userRequester"] = tup[4]
        my_dict["transactionID"] = tup[5]
        my_dict["partID"] = tup[6]
        my_dict["userID"] = tup[7]
        my_dict["warehouseID"] = tup[8]
        return my_dict
    

    def addTransferTransaction(self, data):
        """
        Validates and adds a new transfer transaction.
        """
        response = self._validate_data(data)
        if response.isValid():
            transactionDate, partAmount, toWarehouse, userRequester, partID, warehouseID, userID, toRack = response.value
        else: return response.value

        sender_rackID = self.stored_in_dao.get_rack_with_pid_wid(partID, warehouseID)
        if not sender_rackID:
            return jsonify(Error=f"There is no rack for source warehouse ({warehouseID}) and part ({partID})"), 400

        response = self._validate_enough_quantity_in_warehouse(warehouseID, partID, sender_rackID, partAmount)
        if response.isValid(): sender_parts_total = response.value
        else: return response.value

        response = self._validate_rack_exists(rackID=toRack)
        if not response.isValid(): return response.value

        response = self._validate_rack_is_not_in_use_for_different_part(toRack, toWarehouse, partID)
        if not response.isValid(): return response.value

        rid = StoredInDAO().get_rack_with_pid_wid(pid=partID, wid=toWarehouse)
        if rid and rid != toRack:
            return jsonify(Error=f"Warehouse ({warehouseID}) and part ({partID}) assigned to rack {rid}, not {toRack}"), 400

        # Update part quantity in destination
        to_warehouse_total = self.stored_in_dao.get_quantity(wid=toWarehouse, pid=partID, rid=toRack)
        flag = self.stored_in_dao.modify_quantity(toWarehouse, partID, toRack, to_warehouse_total + partAmount)
        if not flag: return jsonify(Error="Failed to modify destination quantity"), 500

        # Update part quantity of the sender warehouse
        flag = self.stored_in_dao.modify_quantity(warehouseID, partID, sender_rackID, sender_parts_total - partAmount)
        if not flag: return jsonify(Error="Failed to modify source quantity"), 500

        transferid = self.transferTransactionDAO.addTransferTransaction(
                                                    to_warehouse=toWarehouse,
                                                    user_requester=userRequester,
                                                    tdate=transactionDate,
                                                    part_amount=partAmount,
                                                    pid=partID,
                                                    uid=userID,
                                                    wid=warehouseID)
        
        if not transferid: return jsonify(Error="Failed to add transfer transaction"), 500
        data["transferid"] = transferid
        return jsonify(Result=data), 201

    
    def getAllTransferTransaction(self):
        dao = TransferTransactionDAO()
        dbtuples = dao.getAllTransferTransaction()
        if dbtuples:
            result = []
            for tup in dbtuples:
                result.append(self.mapToDict(tup))
            return jsonify(Result=result)
        else:
            return jsonify(Error="Failed to load transfer transaction"), 500
    

    def getTransferTransactionById(self, transferid):
        dao = TransferTransactionDAO()
        dbtuples = dao.getTransferTransactionById(transferid)
        if dbtuples:
            return jsonify(Result=self.mapToDict(dbtuples[0]))
        else:
            return jsonify(Error="Transfer {} does not exist".format(transferid)), 400
        

    def modifyTransferTransactionByID(self, transferid, data):
        """
        Modifies the given transfer transaction.
        Performs basic validation but does not update other tables.
        """
        response = self._validate_data(data)
        if response.isValid():
            transactionDate, partAmount, toWarehouse, userRequester, partID, warehouseID, userID, toRack = response.value
        else: return response.value

        response = self._validate_data(data)
        if response.isValid():
            transactionDate, partAmount, toWarehouse, userRequester, partID, warehouseID, userID, toRack = response.value
        else: return response.value

        sender_rackID = self.stored_in_dao.get_rack_with_pid_wid(partID, warehouseID)
        if not sender_rackID:
            return jsonify(Error=f"There is no rack for source warehouse ({warehouseID}) and part ({partID})"), 400

        response = self._validate_rack_exists(rackID=toRack)
        if not response.isValid(): return response.value

        response = self._validate_rack_is_not_in_use_for_different_part(toRack, toWarehouse, partID)
        if not response.isValid(): return response.value

        rid = StoredInDAO().get_rack_with_pid_wid(pid=partID, wid=toWarehouse)
        if rid and rid != toRack:
            return jsonify(Error=f"Warehouse ({warehouseID}) and part ({partID}) assigned to rack {rid}, not {toRack}"), 400

        dao = TransferTransactionDAO()
        count = dao.modifyTransferTransactionById(to_warehouse=toWarehouse,
                                                  user_requester=userRequester,
                                                  tdate=transactionDate,
                                                  part_amount=partAmount,
                                                  pid=partID,
                                                  uid=userID,
                                                  wid=warehouseID,
                                                  transferid=transferid)
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
            toWarehouse = data["toWarehouse"]
            userRequester = data["userRequester"]
            partID = data["partID"]
            warehouseID = data["warehouseID"]
            userID = data["userID"]
            toRack = data["toRack"]
        except KeyError as e:
            return InvalidResponse(jsonify(Error={"Invalid argument names!": e.args}), 400)
        
        # Check that all fields are integers.
        for key in data:
                if key != "transactionDate" and not isinstance(data[key],int):
                    return InvalidResponse(jsonify(Error='{} has to be a integer.'.format(key)), 400)
        
        # Verify types
        if not isinstance(data["transactionDate"],str):
            return InvalidResponse(jsonify(Error='{} has to be a string.'.format("transactionDate")), 400)
        elif partAmount <= 0:
            return InvalidResponse(jsonify(Error="partAmount must be a positive number greater than 0"), 400)
        elif not self.user_dao.getUserByID(userID):
            return InvalidResponse(jsonify(Error="Invalid Tranfer. The user who sent the transfer does not exist."), 400)
        elif not self.user_dao.getUserByID(userRequester):
            return InvalidResponse(jsonify(Error="Invalid Transfer. The user who requested the transfer does not exist."), 400)
        elif not self.part_dao.searchByID(partID):
            return InvalidResponse(jsonify(Error="Invalid Transfer. The part does not exist."), 400)
        elif not self.warehouse_dao.getWarehouseByID(warehouseID):
            return InvalidResponse(jsonify(Error="Invalid Transfer. The warehouse who sent the transfer does not exist."), 400)
        elif not self.warehouse_dao.getWarehouseByID(toWarehouse):
            return InvalidResponse(jsonify(Error="Invalid Transfer. The warehouse that requested the warehouse does not exist."), 400)
        elif not self.warehouse_dao.worksIn(warehouseID, userID):
            return InvalidResponse(jsonify(Error="Invalid Transfer. The user who sent the transfer does not work in the "
                           "warehouse that will be sending the transfer."), 400)
        elif not self.warehouse_dao.worksIn(toWarehouse, userRequester):
            return InvalidResponse(jsonify(Error="Invalid Transfer. The user who requested the transfer does not work in the "
                           "warehouse that will be receiving the transfer."), 400)
        return ValidResponse(transactionDate, partAmount, toWarehouse, userRequester, partID, warehouseID, userID, toRack)