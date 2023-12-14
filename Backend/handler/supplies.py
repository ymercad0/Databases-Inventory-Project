from flask import jsonify
from Backend.DAOs.supplies import SuppliesDao
from Backend.DAOs.suppliers import SupplierDAO


class SuppliesHandler:
    def mapToDict(self, tup):
        my_dict = {}
        my_dict['sid'] = tup[0]
        my_dict['pid'] = tup[1]
        my_dict['stock'] = tup[2]
        return my_dict

    def mapPartsSupplied(self, tup):
        """Builds dictionary that contains all the information of parts being supplied.

        Args:
            tup (tuple): A record, given as a tuple, from the natural join of parts and supplies tables.

        Returns:
            dict: A dictionary that contains all information mapped to the correct keys, later to be transformed into
            JSON format.
        """
        my_dict = {}
        my_dict['pid'] = tup[0]
        my_dict['Part Name'] = tup[1]
        my_dict['Part Color'] = tup[2]
        my_dict['Part Material'] = tup[3]
        my_dict['MSRP'] = tup[4]
        my_dict['sid'] = tup[5]
        my_dict['stock'] = tup[6]
        return my_dict

    def getPartsSupplied(self, sid):
        """ Returns all information for parts that are being supplied by a given supplier.

        Args:
            sid (int): ID of the supplier that we want to know which parts they are supplying,

        Returns:
            JSON object that contains all information of the parts supplied by the requested supplier.
        """
        # Validate that the sid is an integer
        if not isinstance(sid, int):
            return jsonify(Error="sid has to be an integer."), 400
        # Validate that the supplier exists
        elif not SupplierDAO().searchByID(sid):
            return jsonify(Error="Supplier not found. Give an ID for an existing supplier."), 404

        dao = SuppliesDao()

        tups = dao.get_parts_supplied(sid)
        if not tups:
            return jsonify(Error=f"No parts are being supplied by supplier {sid}."), 404

        res = []

        for tup in tups:
            res.append(self.mapPartsSupplied(tup))
        return jsonify(res), 200
