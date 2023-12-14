from flask import Flask, jsonify, request
from flask_cors import CORS
from Backend import dbconfig as config
# Import handlers
from Backend.handler.outgoingTransaction import OutgoingTransactionHandler
from Backend.handler.parts import PartHandler
from Backend.handler.suppliers import SupplierHandler
from Backend.handler.user_handler import UserHandler
from Backend.handler.warehouse_handler import WarehouseHandler
from Backend.handler.customer import CustomerHandler
from Backend.handler.racks import RackHandler
from Backend.handler.incomingTransaction import IncomingTransactionHandler
from Backend.handler.transferTransaction import TransferTransactionHandler
from Backend.handler.supplies import SuppliesHandler
from Backend.handler.transaction import TransactionHandler


# App initialization
app = Flask(__name__)
app.config.from_object(config)
CORS(app)


@app.route('/')  # default route handler
@app.route('/sqlytes')
def greeting():
    return 'Hello, this is the SQLytes API!'


# route to get all parts or add a part
@app.route('/sqlytes/part', methods=['GET', 'POST'])
def getAllParts():
    if request.method == "GET":
        return PartHandler().getAllParts()
    elif request.method == "POST":  # performs insert queries
        data = request.json
        return PartHandler().insertPart(data)
    else:
        return jsonify('Not supported'), 405


# route to find a specific part
@app.route('/sqlytes/part/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def searchPartByID(pid):
    if request.method == "GET":  # performs select-project-join queries
        return PartHandler().searchByID(pid)
    elif request.method == "PUT":  # performs update queries
        data = request.json
        return PartHandler().updateByID(pid, data)
    elif request.method == "DELETE":  # performs delete queries
        return PartHandler().deleteByID(pid)
    else:
        return jsonify('Not supported'), 405
    
@app.route("/sqlytes/customer", methods=["POST", "GET"])
def allCustomers():
    if request.method == "POST":
        data = request.json
        return CustomerHandler().addCustomer(data)
    elif request.method == "GET":
        return CustomerHandler().getAllCustomers()
    else:
        return jsonify("Not supported"), 405


@app.route("/sqlytes/customer/<int:cid>", methods=["GET", "PUT", "DELETE"])
def customerById(cid):
    if request.method == "GET":
        return CustomerHandler().getCustomerById(cid)
    elif request.method == "PUT":
        data = request.json
        return CustomerHandler().modifyCustomerById(cid, data)
    elif request.method == "DELETE":
        return CustomerHandler().deleteCustomerById(cid)
    else:
        return jsonify("Not supported"), 405


@app.route("/sqlytes/rack", methods=["POST", "GET"])
def allRacks():
    if request.method == "POST":
        data = request.json
        return RackHandler().addRack(data)
    elif request.method == "GET":
        return RackHandler().getAllRacks()
    else:
        return jsonify("Not supported"), 405


@app.route("/sqlytes/rack/<int:rid>", methods=["GET", "PUT", "DELETE"])
def rackById(rid):
    if request.method == "GET":
        return RackHandler().getRackByID(rid)
    elif request.method == "PUT":
        data = request.json
        return RackHandler().updateByID(rid, data)
    elif request.method == "DELETE":
        return RackHandler().deleteByID(rid)
    else:
        return jsonify("Not supported"), 405



@app.route('/sqlytes/supplier', methods=['GET', 'POST'])
def getAllSuppliers():
    if request.method == "GET":
        return SupplierHandler().getAllSuppliers()
    elif request.method == "POST":  # performs insert queries
        data = request.json
        return SupplierHandler().insertSupplier(data)
    else:
        return jsonify('Not supported'), 405


@app.route('/sqlytes/supplier/<int:sid>', methods=['GET', 'PUT', 'DELETE'])
def searchSupplierByID(sid):
    if request.method == "GET":  # performs select-project-join queries
        return SupplierHandler().searchByID(sid)

    elif request.method == "PUT":  # performs update queries
        data = request.json
        return SupplierHandler().updateByID(sid, data)

    elif request.method == "DELETE":  # performs delete queries
        return SupplierHandler().deleteByID(sid)

    else:
        return jsonify('Not supported'), 405

@app.route('/sqlytes/supplies/<int:sid>', methods=['GET'])
def getPartsSupplied(sid):
    """ Lets you see all parts that are being supplied
        by a supplier.
    """
    if request.method == "GET":
        return SuppliesHandler().getPartsSupplied(sid)
    else:
        return jsonify("Not Supported"), 405

    
@app.route('/sqlytes/user',methods=['GET','POST'])
def getUsers():
    """Returns all users from the Users Table in the database 
       or it creates a new user in the Users Table
    """
    if request.method == "GET": # Performs the select-project-join queries.
        return UserHandler().getAllUsers()
    elif request.method == "POST":
        return UserHandler().insertUser(request.json)
    else:
        return jsonify(Error='Method not allowed'), 405
    
@app.route('/sqlytes/user/<int:uid>', methods=['GET','PUT','DELETE'])
def getUserById(uid: int):
    if request.method == 'GET':
        return UserHandler().getUserByID(uid)
    elif request.method == 'PUT':
        return UserHandler().updateUserByID(uid,request.json)
    elif request.method == 'DELETE':
        return UserHandler().deleteUserByID(uid)
    else:
        return jsonify(Error='Method not allowed'), 405

@app.route('/sqlytes/warehouse', methods=['GET','POST'])
def getWarehouses():
    if request.method == 'GET':
        return WarehouseHandler().getAllWarehouses()
    elif request.method == 'POST':
        return WarehouseHandler().insertWarehouse(request.json)
    else:
        return jsonify(Error='Method not allowed'), 405
    
    
@app.route('/sqlytes/warehouse/<int:wid>', methods=['GET','PUT','DELETE'])
def getWarehouseById(wid: int):
    if request.method == 'GET':
        return WarehouseHandler().getWarehouseById(wid)
    elif request.method == 'PUT':
        return WarehouseHandler().updateWarehouseByID(wid,request.json)
    elif request.method == 'DELETE':
        return WarehouseHandler().deleteWarehouseByID(wid)
    else:
        return jsonify(Error='Method not allowed'), 405
    


@app.route("/sqlytes/incoming", methods=["POST", "GET"])
def allIncomingTransactions():
    try:
        if request.method == "POST":
            data = request.json
            return IncomingTransactionHandler().addIncomingTransaction(data)
        elif request.method == "GET":
            return IncomingTransactionHandler().getAllIncomingTransaction()
        else:
            return jsonify(Error="Not supported"), 405
    except Exception as e:
        print(e)
        return jsonify(Error="An unkown error occurred"), 500


@app.route("/sqlytes/incoming/<int:itid>", methods=["GET", "PUT"])
def incomingTransactionById(itid):
    try:
        if request.method == "GET":
            return IncomingTransactionHandler().getIncomingTransactionById(itid)
        elif request.method == "PUT":
            data = request.json
            return IncomingTransactionHandler().modifyIncomingTransactionByID(itid, data)
        else:
            return jsonify(Error="Not supported"), 405
    except Exception as e:
        print(e)
        return jsonify(Error="An unkown error occurred"), 500
    


@app.route("/sqlytes/outgoing", methods=["POST", "GET"])
def allOutgoingTransactions():
    try:
        if request.method == "POST":
            data = request.json
            return OutgoingTransactionHandler().addOutgoingTransaction(data)
        elif request.method == "GET":
            return OutgoingTransactionHandler().getAllOutgoingTransaction()
        else:
            return jsonify(Error="Not supported"), 405
    except Exception as e:
        print(e)
        return jsonify(Error="An unkown error occurred"), 500



@app.route("/sqlytes/outgoing/<int:otid>", methods=["GET", "PUT"])
def outgoingTransactionById(otid):
    try:
        if request.method == "GET":
            return OutgoingTransactionHandler().getOutgoingTransactionById(otid)
        elif request.method == "PUT":
            data = request.json
            return OutgoingTransactionHandler().modifyOutgoingTransactionByID(otid, data)
        else:
            return jsonify(Error="Not supported"), 405
    except Exception as e:
        print(e)
        return jsonify(Error="An unkown error occurred"), 500




@app.route("/sqlytes/exchange", methods=["POST", "GET"])
def allTransferTransactions():
    try:
        if request.method == "POST":
            data = request.json
            return TransferTransactionHandler().addTransferTransaction(data)
        elif request.method == "GET":
            return TransferTransactionHandler().getAllTransferTransaction()
        else:
            return jsonify(Error="Not supported"), 405
    except Exception as e:
        print(e)
        return jsonify(Error="An unkown error occurred"), 500



@app.route("/sqlytes/exchange/<int:transferid>", methods=["GET", "PUT"])
def transferTransactionById(transferid):
    try:
        if request.method == "GET":
            return TransferTransactionHandler().getTransferTransactionById(transferid)
        elif request.method == "PUT":
            data = request.json
            return TransferTransactionHandler().modifyTransferTransactionByID(transferid, data)
        else:
            return jsonify(Error="Not supported"), 405
    except Exception as e:
        print(e)
        return jsonify(Error="An unkown error occurred"), 500

    

@app.route("/sqlytes/transaction", methods=["GET", "PUT"])
def allTransactions():
    try:
        if request.method == "GET":
            return TransactionHandler().getAllTransactions()
        elif request.method == "PUT":
            data = request.json
            return TransactionHandler().getTransactionsByWarehouse(data)
        else:
            return jsonify(Error="Not supported"), 405
    except Exception as e:
        print(e)
        return jsonify(Error="An unkown error occurred"), 500


@app.route("/sqlytes/transaction/<int:tid>", methods=["GET"])
def transactionByID(tid):
    try:
        if request.method == "GET":
            return TransactionHandler().getTransactionById(tid)
        else:
            return jsonify(Error="Not supported"), 405
    except Exception as e:
        print(e)
        return jsonify(Error="An unkown error occurred"), 500


# Global Statistics
@app.route("/sqlytes/most/rack", methods=["GET"])
def warehousesWithMostRacks():
    if request.method == "GET":
        return WarehouseHandler().getTopRacks()
    else:
        return jsonify("Not supported"), 405

@app.route("/sqlytes/most/deliver", methods=["GET"])
def warehousesWithMostTransfers():
    if request.method == "GET":
        return WarehouseHandler().getTopExchanges()
    else:
        return jsonify("Not supported"), 405

@app.route("/sqlytes/least/outgoing", methods=["GET"])
def warehousesWithLeastOutgoing():
    if request.method == "GET":
        return WarehouseHandler().getLeastOutgoing()
    else:
        return jsonify("Not supported"), 405

@app.route("/sqlytes/most/incoming", methods=["GET"])
def warehousesWithMostIncoming():
    if request.method == "GET":
        return WarehouseHandler().getTopIncoming()
    else:
        return jsonify("Not Supported"), 405

@app.route("/sqlytes/most/transactions", methods=["GET"])
def usersWithMostTransactions():
    if request.method == "GET":
        return WarehouseHandler().getTopUserTransactions()
    else:
        return jsonify("Not Supported"), 405

@app.route("/sqlytes/most/city", methods=["GET"])
def warehouseMostCityTransactions():
    if request.method == "GET":
        return WarehouseHandler().getTopCity()
    else:
        return jsonify("Not Supported"), 405


# Local Statistics
@app.route("/sqlytes/warehouse/<int:wid>/profit", methods=["POST"])
def warehouseProfit(wid):
    if request.method == "POST":
        return WarehouseHandler().getYearlyProfit(wid, request.json)
    else:
        return jsonify("Not Supported"), 405

@app.route("/sqlytes/warehouse/<int:wid>/rack/material", methods=["POST"])
def warehouseBottomRacks(wid):
    if request.method == "POST":
        return WarehouseHandler().getBottomRacks(wid, request.json)
    else:
        return jsonify("Not Supported"), 405

@app.route("/sqlytes/warehouse/<int:wid>/users/receivesmost", methods=["POST"])
def warehouseTopUserExchanges(wid):
    if request.method == "POST":
        return WarehouseHandler().getTopUserExchanges(wid, request.json)
    else:
        return jsonify("Not Supported"), 405

@app.route("/sqlytes/warehouse/<int:wid>/rack/expensive", methods=["POST"])
def warehouseTopExpensiveRacks(wid):
    if request.method == "POST":
        return WarehouseHandler().getTopExpensiveRacks(wid, request.json)
    else:
        return jsonify("Not Supported"), 405

@app.route("/sqlytes/warehouse/<int:wid>/transaction/suppliers", methods=["POST"])
def warehouseTopSuppliers(wid):
    if request.method == "POST":
        return WarehouseHandler().getTopSuppliers(wid, request.json)
    else:
        return jsonify("Not Supported"), 405

@app.route("/sqlytes/warehouse/<int:wid>/transaction/leastcost", methods=["POST"])
def warehouseSmallestIncomingCost(wid):
    if request.method == "POST":
        return WarehouseHandler().getLowestDayCost(wid, request.json)
    else:
        return jsonify("Not Supported"), 405

@app.route("/sqlytes/warehouse/<int:wid>/rack/lowstock", methods=["POST"])
def warehouseLowestStockRack(wid):
    if request.method == "POST":
        return WarehouseHandler().getLowestRackStock(wid, request.json)
    else:
        return jsonify("Not Supported"), 405


# Voila
@app.route("/sqlytes/warehouse/<int:wid>/parts", methods=["GET"])
def warehouseParts(wid):
    if request.method == "GET":
        return WarehouseHandler().getAllWarehouseParts(wid)
    else:
        return jsonify("Not Supported"), 405

@app.route("/sqlytes/warehouse/<int:uid>/worksin/<int:wid>/", methods=["GET"])
def userWorksInWarehouse(wid, uid):
    if request.method == "GET":
        return WarehouseHandler().works_in(wid, uid)
    else:
        return jsonify("Not Supported"), 405


if __name__ == '__main__':
    app.run()
