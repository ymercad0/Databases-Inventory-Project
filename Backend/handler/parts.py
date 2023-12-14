from flask import jsonify
from Backend.DAOs.parts import PartDAO


class PartHandler:
    """
    this should:
    * connect to the DB
    * extract the list of parts
    * take those records,
    * and make them a JSON
    """
    def getAllParts_old(self):
        result = []
        result.append({'id': 2, 'name': 'tuerca','color': 'blue'})
        result.append({'id': 4, 'name': 'clavo','color': 'gray'})
        return jsonify(result)

    def mapToDict(self, tup):
        # this is kind of getting hardcoded, because we have to know the order in which we want the query
        # tuples are every record, so this just maps the records into dictionaries
        # if the query changes, we have to change mapToDict. We have to have a constructor for each class
        my_dict = {}
        my_dict['id'] = tup[0]
        my_dict['Name'] = tup[1]
        my_dict['Color'] = tup[2]
        my_dict['Material'] = tup[3]
        my_dict['msrp'] = tup[4]
        return my_dict
    
    def mapToDictAllParts(self, tup):
        # this is kind of getting hardcoded, because we have to know the order in which we want the query
        # tuples are every record, so this just maps the records into dictionaries
        # if the query changes, we have to change mapToDict. We have to have a constructor for each class
        my_dict = {}
        my_dict['id'] = tup[0]
        my_dict['Name'] = tup[1]
        my_dict['Color'] = tup[2]
        my_dict['Material'] = tup[3]
        my_dict['msrp'] = tup[4]
        my_dict['Part Quantity'] = tup[5]
        return my_dict

    def getAllParts(self):
        dao = PartDAO()
        # data access object: design pattern that captures, in an object, the query to be sent to the DB
        dbtuples = dao.getAllParts()  # this should return an array of Tuples

        result = []
        # loop thru each tuple and turn them into a dictionary (serialization)
        for tup in dbtuples:
            result.append(self.mapToDict(tup))
        return jsonify(result)

    def searchByID(self, pid):
        dao = PartDAO()
        result = dao.searchByID(pid)  # if this is null, then the part with that id doesn't exist
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return jsonify(Error=f"Did not find a part with id: {pid}"), 404

    def insertPart(self, data):
        # print(data)
        if len(data) != 4:
            return jsonify(Error="Did not receive the correct amount of information needed for a Part record."), 400

        # looking up the values in the dict
        try:
            name = data['Name']
            color = data['Color']
            material = data['Material']
            msrp = data['msrp']
        except:
            return jsonify(Error="Invalid argument names!"), 400

        if not isinstance(name, str):
            return jsonify(Error=f"Error: The inputted name '{name}' is not a string!"), 400
        if not isinstance(color, str):
            return jsonify(Error=f"Error: The inputted color '{color}' is not a string!"), 400
        if not isinstance(material, str):
            return jsonify(Error=f"Error: The inputted material '{material}' is not a string!"), 400
        if not isinstance(msrp, float) and not isinstance(msrp, int):
            return jsonify(Error=f"Error: The inputted msrp '{msrp}' is not a valid number!"), 400
        if msrp <= 0:
            return jsonify(Error=f"Error: The market sale retail price (msrp) entered has to be bigger than 0"), 400

        if name and color and material and msrp:
            dao = PartDAO()
            pid = dao.insertPart(name, color, material, msrp)
            data['pid'] = pid
            return jsonify(data), 201
        else:
            return jsonify(Error="Unexpected attribute values."), 400

    def deleteByID(self, pid):
        # Can't delete a part that is being supplied
        dao = PartDAO()

        in_stock = dao.inStock(pid)
        if in_stock:
            return jsonify(Error="Cannot delete this part, since it is currently being supplied."), 400

        # Can't delete a part that is being referenced in a transaction
        in_transaction = dao.inTransaction(pid)
        if in_transaction:
            return jsonify(Error="Cannot delete this part, since it is being referenced in a past transaction."), 400

        being_stored = dao.beingStored(pid)
        if being_stored:
            return jsonify(Error="Cannot delete this part, since it is currently being stored in a warehouse."), 400

        result = dao.deleteByID(pid)  # if this is null, then the part with that id doesn't exist
        if result:
            return jsonify(f"Deleted part with id: {pid}"), 200
        else:
            return jsonify(Error=f"Did not find a part with id:{pid}"), 404

    def updateByID(self, pid, data):

        if len(data) != 5 and len(data) != 4:
            return jsonify(Error="Did not receive the correct amount of information needed for a Part record."), 400
        # looking up the values in the dict
        try:
            name = data['Name']
            color = data['Color']
            material = data['Material']
            msrp = data['msrp']
        except:
            return jsonify(Error="Invalid argument names!"), 400


        if not isinstance(name, str):
            return jsonify(Error=f"The inputted name '{name}' is not a string!"), 400
        if not isinstance(color, str):
            return jsonify(Error=f"The inputted color '{color}' is not a string!"), 400
        if not isinstance(material, str):
            return jsonify(Error=f"The inputted material '{material}' is not a string!"), 400
        if not isinstance(msrp, float) and not isinstance(msrp, int):
            return jsonify(Error=f"The inputted msrp '{msrp}' is not a valid number!"), 400
        if msrp <= 0:
            return jsonify(Error=f"The market sale retail price (msrp) entered has to be bigger than 0"), 400

        if pid and name and color and material and msrp:
            dao = PartDAO()
            flag = dao.updateByID(pid, name, color, material, msrp)
            if flag:
                return jsonify(data), 200
            else:
                return jsonify(Error=f"Did not find a part with id: {pid}"), 404
        else:
            return jsonify(Error="Unexpected attribute values."), 400