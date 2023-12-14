from Backend.DAOs.racks import RackDAO
from Backend.DAOs.parts import PartDAO
from Backend.DAOs.warehouse_dao import WarehouseDAO
from Backend.DAOs.stored_in import StoredInDAO
from flask import jsonify


class RackHandler:
    def mapToDict(self, tup):
        my_dict = {}
        my_dict['id'] = tup[0]
        my_dict['Name'] = tup[1]
        my_dict['Capacity'] = tup[2]
        return my_dict

    def getAllRacks(self):
        dao = RackDAO()
        tups = dao.getAllRacks()
        res = []
        for tup in tups:
            res.append(self.mapToDict(tup))
        return jsonify(res)

    def addRack(self, data):
        if len(data) != 2:
            return jsonify(Error="Did not receive the correct amount of information needed for a Rack record. Need the "
                           "following data: rack name (name), capacity"), 400

        try:
            name = data["Name"]
            capacity = data["Capacity"]
        except:
            return jsonify(Error="Invalid argument names!"), 400

        if not isinstance(name, str):
            return jsonify(Error=f"The inputted name '{name}' is not a string!"), 400
        if not isinstance(capacity, int):
            return jsonify(Error=f"The inputted capacity '{capacity}' is not a valid integer!"), 400
        if capacity <= 0:
            return jsonify(Error=f"The rack must have a capacity bigger than 0."), 400

        if name and capacity:
            dao = RackDAO()

            rid = dao.addRack(name, capacity)
            data['rid'] = rid
            return jsonify(data), 201
        else:
            return jsonify(Error="Unexpected attribute values."), 400

    def getRackByID(self, rid):
        dao = RackDAO()
        tups = dao.getRackById(rid)
        if tups:
            return jsonify(self.mapToDict(tups))
        else:
            return jsonify(Error=f"Could not find a rack with id: {rid}"), 404

    def deleteByID(self, rid):
        dao = RackDAO()

        stores_parts = dao.stores_parts(rid)
        if stores_parts:
            return jsonify(Error="Cannot delete this rack, since it is currently storing parts in it."), 400

        in_transaction = dao.in_incoming_transaction(rid)
        if in_transaction:
            return jsonify(Error="Cannot delete this rack, since it is being referenced in a transaction."), 400

        res = dao.deleteRackById(rid)
        if res:
            return jsonify(Error=f'Deleted rack with id: {rid}'), 200
        else:
            return jsonify(Error=f"Could not find a rack with rack id: {rid}"), 404

    def updateByID(self, rid, data):
        if len(data) != 3 and len(data) != 2:
            return jsonify("Error: Did not receive the correct amount of information needed for a Rack record."), 400

        try:
            name = data['Name']
            capacity = data['Capacity']
        except:
            return jsonify(Error="Invalid argument names!"), 400

        if not isinstance(name, str):
            return jsonify(Error=f"The inputted name '{name}' is not a string!"), 400
        if not isinstance(capacity, int):
            return jsonify(Error=f"The inputted capacity '{capacity}' is not an integer!"), 400

        # check if capacity is valid
        if capacity <= 0:
            return jsonify(Error=f"The rack must have a capacity bigger than 0."), 400

        # check how many parts is this rack currently holding (if it is in stored in. If it's not, qty will be 0)
        qty = StoredInDAO().get_qty_with_rid(rid)
        if capacity < qty:
            return jsonify(Error=f"Cannot update capacity since this new capacity ({capacity}) is less than the amount"
                           f" of parts that this rack is currently holding ({qty}). New capacity must be more than "
                           f"{qty}."), 400

        if rid and name and capacity:
            dao = RackDAO()
            flag = dao.modifyRackById(rid, name, capacity)
            if flag:
                return jsonify(data), 200
            else:
                return jsonify(Error=f"Could not find a rack with rack id: {rid}"), 404
        else:
            return jsonify(Error="Unexpected attribute values."), 400
