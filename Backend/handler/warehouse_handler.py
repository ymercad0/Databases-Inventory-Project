from typing import Iterable
from flask import jsonify
from Backend.DAOs.warehouse_dao import WarehouseDAO
from Backend.handler.parts import PartHandler


class WarehouseHandler:
    """WarehouseHandler takes care of managing the communication between the
    request and the database for the warehouses route."""

    def __init__(self):
        self.warehouseDAO = WarehouseDAO()
        self.parts_handler = PartHandler()

    def build_warehouse_dict(self, row: tuple) -> dict:
        """Builds dictionary that contains
        all the information from a warehouse.

        Args:
            row (tuple): A record, given as a tuple, from the
        Warehouses table in the database.

        Returns:
            dict: A dictionary that contains all the information mapped to
        the correct keys. This is so that later the dictionary can be
        transformed into JSON format.
        """
        warehouse_dict = {}
        warehouse_dict['wid'] = row[0]
        warehouse_dict['wname'] = row[1]
        warehouse_dict['wcountry'] = row[2]
        warehouse_dict['wregion'] = row[3]
        warehouse_dict['wcity'] = row[4]
        warehouse_dict['wstreet'] = row[5]
        warehouse_dict['wzipcode'] = row[6]
        warehouse_dict['wbudget'] = row[7]
        return warehouse_dict

    @staticmethod
    def _build_statistics_dict(results: Iterable, dict_name: str, dict_val_names: tuple) -> dict:
        """Constructs a dictionary for the local/global statistics based on the results
        returned from a query, the name of the dict, and the name of each value in the dict."""
        values = []
        for res in results:
            mapped_values = {}
            if len(res) != len(dict_val_names):
                raise ValueError(f"There are more row names than value names! Error building '{dict_name}' dictionary.")
            for i in range(len(res)):
                mapped_values[dict_val_names[i]] = res[i]
            values.append(mapped_values)
        return {dict_name: values}

    def getAllWarehouses(self):
        """Returns all warehouses from the Warehouses Table in the database.

        Return: JSON object that contains all the warehouses from the Warehouses Table that were found in the database.
        """

        all_warehouses_tuples = self.warehouseDAO.getAllWarehouses()
        all_warehouses_result = []
        for record in all_warehouses_tuples:
            all_warehouses_result.append(self.build_warehouse_dict(record))
        return jsonify(Warehouses=all_warehouses_result)

    def insertWarehouse(self, data) -> object:
        """Insert a new warehouse in the Warehouses Table in the database.

        Keyword arguments:
        argument: Data to be sent to the DAO.
        Return: JSON object that contains the warehouse ID that was inserted.
        """
        # Check that we received the expect quantity of data.
        if len(data) != 7:
            return jsonify(Error='Missing data to insert a warehouse.'), 400

        # Handle that the keys are valid.
        try:
            warehouse_name = data['wname']
            warehouse_country = data['wcountry']
            warehouse_region = data['wregion']
            warehouse_city = data['wcity']
            warehouse_street = data['wstreet']
            warehouse_zipcode = data['wzipcode']
            warehouse_budget = data['wbudget']
        except KeyError:
            return jsonify(
                Error='Unexpected or Incorrect attribute in post request. Check that the fields of the request are correct'), 400

        # Check that there are no empty attributes and return which noe failed to the client.
        for key in data:
            if not data[key]:
                return jsonify(Error='Missing ' + key + ' attribute'), 400

        # Check that all fields except budget are strings.
        for key in data:
            if key != 'wbudget' and not isinstance(data[key], str):
                return jsonify(Error='{} has to be a string.'.format(key)), 400

        # Check that budget is a double.
        if not isinstance(warehouse_budget, float):
            return jsonify(Error='Field {} has to be a double'.format(warehouse_budget)), 400

        # Budget can not be a negative value or zero.
        elif warehouse_budget <= 0:
            return jsonify(Error='Budget can not be a value less or equal to 0'), 400

        warehouse_with_name_and_city_exists = self.warehouseDAO.name_city_combo_exists(wname=warehouse_name,
                                                                                       wcity=warehouse_city)
        if warehouse_with_name_and_city_exists is None:
            return jsonify(Error='Failed to validate against existing warehouses'), 500
        elif warehouse_with_name_and_city_exists:
            return jsonify(
                Error=f'Can only have 1 warehouse with name ({warehouse_name}) in city ({warehouse_city})'
            ), 400

        wid = self.warehouseDAO.insertWarehouse(warehouse_name,
                                                warehouse_country,
                                                warehouse_region,
                                                warehouse_city,
                                                warehouse_street,
                                                warehouse_zipcode,
                                                warehouse_budget)
        if not wid:
            return jsonify(Error='Failed to add warehouse'), 500
        data['wid'] = wid
        return jsonify(data), 201

    def getWarehouseById(self, wid: int) -> object:
        """Execute a query to get a warehouse from the Warehouses Table in the database with the given ID.

        Args:
            wid (int): ID of the warehouse to be searched for.

        Returns:
            object: JSON object that contains all the data found of the warehouse with the given ID.
        """
        warehouse_tuple = self.warehouseDAO.getWarehouseByID(wid)
        if not warehouse_tuple:
            return jsonify(Error='Warehouse Not Found. Give an ID for an existing warehouse.'), 404
        else:
            warehouse = self.build_warehouse_dict(warehouse_tuple[0])
            return jsonify(Warehouse=warehouse)

    def updateWarehouseByID(self, wid: int, data: object) -> object:
        """Update a warehouse in the Warehouses Table in the database by the given ID.

        Args:
            wid (int): ID of the warehouse to be deleted.
            data (object): JSON object containing information of the warehouse to be updated.

        Returns:
            ID of the user that was updated in JSON format.
        """
        # Check that we received the expect quantity of data.
        if len(data) != 7:
            return jsonify(Error='Incorrect amount of data has been sent.'), 400

        # Handle that the keys are valid.
        try:
            warehouse_name = data['wname']
            warehouse_country = data['wcountry']
            warehouse_region = data['wregion']
            warehouse_city = data['wcity']
            warehouse_street = data['wstreet']
            warehouse_zipcode = data['wzipcode']
            warehouse_budget = data['wbudget']
        except KeyError:
            return jsonify(Error='Unexpected or Incorrect attribute in post request'), 400

        # Check that there are no empty attributes and return which noe failed to the client.
        for key in data:
            if not data[key]:
                return jsonify(Error='Missing ' + key + ' attribute'), 400

        # Check that all fields except budget are strings.
        for key in data:
            if key != 'wbudget' and not isinstance(data[key], str):
                return jsonify(Error='{} has to be a string.'.format(key)), 400

        # Check that budget is a double.
        if not isinstance(warehouse_budget, float):
            return jsonify(Error='Field {} has to be a double'.format(warehouse_budget)), 400

        # Budget can not be a negative value or zero.
        elif warehouse_budget <= 0:
            return jsonify(Error='Budget can not be a value less or equal to 0'), 400

        warehouse_with_name_and_city_exists = self.warehouseDAO.name_city_combo_exists(wname=warehouse_name,
                                                                                       wcity=warehouse_city)
        if warehouse_with_name_and_city_exists is None:
            return jsonify(Error='Failed to validate against existing warehouses'), 500
        elif warehouse_with_name_and_city_exists:
            return jsonify(
                Error=f'Can only have 1 warehouse with name ({warehouse_name}) in city ({warehouse_city})'
            ), 400

        flag = self.warehouseDAO.updateWarehouseByID(wid, warehouse_name, warehouse_country, warehouse_region,
                                                     warehouse_city,
                                                     warehouse_street, warehouse_zipcode, warehouse_budget)
        if flag:
            return jsonify(data), 200
        else:
            return jsonify(Error='Warehouse Not Found'), 404

    def deleteWarehouseByID(self, wid: int) -> object:
        """Delete a warehouse from the Warehouses Table in the database by the given ID.

        Args:
            wid (int): ID of the warehouse to be deleted.

        Returns:
            ID of the warehouse that was deleted in JSON format.
        """
        if not wid:
            return jsonify(Error='wid was not passed to the request (wid is 0)'), 400
        elif not self.warehouseDAO.getWarehouseByID(wid):
            return jsonify(Error='Warehouse Not Found.'), 404
        elif not self.warehouseDAO.warehouseInUsers(wid):
            return jsonify(Error='Cannot Delete Warehouse that has active users.'), 400
        elif not self.warehouseDAO.warehouseInTransactions(wid):
            return jsonify(Error='Cannot Delete Warehouse that has transactions records.'), 400
        elif not self.warehouseDAO.warehouseInTransfer(wid):
            return jsonify(Error='Cannot Delete Warehouse that has transfers records.'), 400
        elif not self.warehouseDAO.warehouseInStoredIn(wid):
            return jsonify(Error='Cannot Delete Warehouse that has racks.'), 400
        else:
            result = self.warehouseDAO.deleteWarehouseByID(wid)
            if not result:
                return jsonify(Error='Unexpected Error.'), 404
            return jsonify(Message='Warehouse {} deleted succesfully'.format(wid)), 200

    # Statistics
    def getTopRacks(self):
        """Part of the global statistics. Gets the top 10 warehouses with the most racks."""
        rack_results = self.warehouseDAO.get_top_racks()
        if not rack_results:
            return jsonify(Error='No results were returned.'), 404
        else:
            rows = ("Warehouse", "Rack Count")
            rack_results = self._build_statistics_dict(rack_results, "Top Racks per Warehouse", rows)
            return jsonify(rack_results), 200

    def getTopExchanges(self):
        """Part of the global statistics. Gets the top 5 warehouses
        with the most exchanges/transfers."""
        transfer_results = self.warehouseDAO.get_most_exchanges()
        if not transfer_results:
            return jsonify(Error='No results were returned.'), 404
        else:
            rows = ("Warehouse", "Total Transfers")
            transfer_results = self._build_statistics_dict(transfer_results, "Most Transfers", rows)
            return jsonify(transfer_results), 200

    def getTopUserTransactions(self):
        """Part of the global statistics. Gets the top 3 users that made the most transactions."""
        transaction_results = self.warehouseDAO.get_top_user_transactions()
        if not transaction_results:
            return jsonify(Error='No results were returned.'), 404
        else:
            rows = ("First Name", "Last Name", "Transaction Count")
            transaction_results = self._build_statistics_dict(transaction_results, "Top User Transactions", rows)
            return jsonify(transaction_results), 200

    def getLeastOutgoing(self):
        """Part of the global statistics. Gets the top 3 warehouses
        with the least outgoing transactions."""
        outgoing_results = self.warehouseDAO.get_least_outgoing()
        if not outgoing_results:
            return jsonify(Error='No results were returned.'), 404
        else:
            rows = ("Warehouse", "Total Outgoing Transactions")
            outgoing_results = self._build_statistics_dict(outgoing_results, "Least Outgoing Transactions", rows)
            return jsonify(outgoing_results), 200

    def getTopIncoming(self):
        """Part of the global statistics. Top 5 warehouses with the most incoming transactions."""
        incoming_results = self.warehouseDAO.get_most_incoming()
        if not incoming_results:
            return jsonify(Error='No results were returned.'), 404
        else:
            rows = ("Warehouse", "Total Incoming Transactions")
            incoming_results = self._build_statistics_dict(incoming_results, "Most Incoming Transactions", rows)
            return jsonify(incoming_results), 200

    def getTopCity(self):
        """Part of the global statistics. Top 3 warehouse cities with the most transactions."""
        city_results = self.warehouseDAO.get_most_city()
        if not city_results:
            return jsonify(Error='No results were returned.'), 404
        else:
            rows = ("Warehouse City", "Total Transactions")
            city_results = self._build_statistics_dict(city_results, "Most Transactions per City", rows)
            return jsonify(city_results), 200

    # Local statistics
    def _validate_user(self, data: object, wid: int) -> dict:
        """Helps encapsulate the code for verifying whether
        a valid user can access the local warehouse statistics."""
        response = dict.fromkeys(['error', 'user_permissions'])
        if type(wid) != int:
            error = f"Invalid argument type! Expected 'int' for a warehouse ID but received {type(wid)}."
            response['error'] = jsonify(Error=error), 400
            return response

        try:
            uid = data['user']
        except:
            response['error'] = jsonify(Error="Invalid argument! Couldn't process the 'User' field."), 400
            return response

        if type(uid) != int:
            error = f"Invalid argument type! Expected 'int' for a user ID but received {type(uid)}."
            response['error'] = jsonify(Error=error), 400
            return response

        has_access = WarehouseDAO().worksIn(wid, uid)
        if not has_access:
            error = f"User #{uid} can't work in Warehouse #{wid}."
            response['error'] = jsonify(Error=error), 404
        else:
            response['user_permissions'] = True
        return response

    def getYearlyProfit(self, wid: int, data: object) -> object:
        """Part of the local statistics. Specifies warehouse's profit by year."""
        # Verify if the user can access this resource
        user_perms = self._validate_user(data, wid)
        if user_perms['error']:
            return user_perms['error']

        elif user_perms['user_permissions']:
            profit_results = self.warehouseDAO.get_profit_yearly(wid)
            if not profit_results:
                return jsonify(Error='No results were returned.'), 404
            else:
                rows = ("Year", "Warehouse", "Net Profit")
                profit_results = self._build_statistics_dict(profit_results, "Yearly Profit", rows)
                return jsonify(profit_results), 200

    # Statistics
    def getBottomRacks(self, wid: int, data: object) -> object:
        """Part of the local statistics. Returns bottom 3 racks by material/type in a warehouse."""
        user_perms = self._validate_user(data, wid)
        if user_perms['error']:
            return user_perms['error']

        elif user_perms['user_permissions']:
            bottom_rack_results = self.warehouseDAO.get_bottom_racks(wid)
            if not bottom_rack_results:
                return jsonify(Error='No results were returned.'), 404
            else:
                rows = ("Part", "Type", "Part Count")
                bottom_rack_results = self._build_statistics_dict(bottom_rack_results, "Bottom Racks", rows)
                return jsonify(bottom_rack_results), 200

    def getTopUserExchanges(self, wid: int, data: object) -> object:
        """Part of the local statistics. Returns top 3 users that received the most
        exchanges from a warehouse."""
        user_perms = self._validate_user(data, wid)
        if user_perms['error']:
            return user_perms['error']

        elif user_perms['user_permissions']:
            user_results = self.warehouseDAO.get_most_user_exchanges(wid)
            if not user_results:
                return jsonify(Error='No results were returned.'), 404
            else:
                rows = ("First Name", "Last Name", "Transfer Count")
                user_results = self._build_statistics_dict(user_results, "Most User Exchanges", rows)
                return jsonify(user_results), 200

    def getTopExpensiveRacks(self, wid: int, data: object) -> object:
        """Part of the local statistics. Top 5 most expensive racks in the warehouse."""
        user_perms = self._validate_user(data, wid)
        if user_perms['error']:
            return user_perms['error']

        elif user_perms['user_permissions']:
            rack_results = self.warehouseDAO.get_most_expensive_racks(wid)
            if not rack_results:
                return jsonify(Error='No results were returned.'), 404
            else:
                rows = ("Warehouse", "Rack", "Rack Price")
                rack_results = self._build_statistics_dict(rack_results, "Most Expensive Racks", rows)
                return jsonify(rack_results), 200

    def getLowestDayCost(self, wid: int, data: object) -> object:
        """Part of the local statistics. Top 3 days with the smallest incoming transactions’ cost."""
        user_perms = self._validate_user(data, wid)
        if user_perms['error']:
            return user_perms['error']

        elif user_perms['user_permissions']:
            day_results = self.warehouseDAO.get_least_daily_cost(wid)
            if not day_results:
                return jsonify(Error='No results were returned.'), 404
            else:
                rows = ("Transaction Date", "Total Incoming Cost")
                day_results = self._build_statistics_dict(day_results, "Least Incoming Trans. Costs", rows)
                return jsonify(day_results), 200

    def getLowestRackStock(self, wid: int, data: object) -> object:
        """Part of the local statistics. Top 5 racks with quantity under the 25% capacity threshold."""
        user_perms = self._validate_user(data, wid)
        if user_perms['error']:
            return user_perms['error']

        elif user_perms['user_permissions']:
            stock_results = self.warehouseDAO.get_least_rack_stock(wid)
            if not stock_results:
                return jsonify(Error='No results were returned.'), 404
            else:
                rows = ("Rack", "Low Capacity Threshold", "Parts Quantity")
                stock_results = self._build_statistics_dict(stock_results, "Lowest Threshold Racks", rows)
                return jsonify(stock_results), 200

    def getTopSuppliers(self, wid: int, data: object) -> object:
        """Part of the local statistics. Top 3 suppliers that supplied to the given warehouse."""
        user_perms = self._validate_user(data, wid)
        if user_perms['error']:
            return user_perms['error']

        elif user_perms['user_permissions']:
            supplier_results = self.warehouseDAO.get_most_suppliers(wid)
            if not supplier_results:
                return jsonify(Error='No results were returned.'), 404
            else:
                rows = ("Supplier Name", "Supply Count")
                supplier_results = self._build_statistics_dict(supplier_results, "Top Warehouse Suppliers", rows)
                return jsonify(supplier_results), 200

    def getAllWarehouseParts(self,wid:int) -> object:
        """Return all parts information for a given warehouse.
        
        Arguments:
        wid(int): ID of the warehouse to return the parts from.
        Return: JSON object that contains all the parts from the warehouse.
        """
        
        # Validate that the wid is an integer.
        if not isinstance(wid, int):
            return jsonify(Error='wid has to be an integer.'), 400
        # Validate the wid is a valid integer.
        elif wid <= 0:
            return jsonify(Error='wid has to be a positive integer.'), 400
        # Validate that the warehouse exists.
        elif not self.warehouseDAO.getWarehouseByID(wid):
            return jsonify(Error='Warehouse Not Found. Give an ID for an existing warehouse.'), 404
        else:
            all_parts = self.warehouseDAO.getAllWarehouseParts(wid)
            if not all_parts:
                return jsonify(Error='No parts were found in the warehouse.'), 404
            else:
                result = []
                for tup in all_parts:
                    result.append(self.parts_handler.mapToDictAllParts(tup)) 
                return jsonify(WarehouseParts=result), 200

    # Voila
    def works_in(self, wid: int, uid: int) -> bool:
        if type(wid) != 'int' and type(uid) != 'int':
            raise TypeError("Invalid types! All IDs must be ints.")

        return WarehouseDAO().worksIn(wid, uid)

