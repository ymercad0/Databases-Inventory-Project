from enum import Enum
from typing import Any
from flask import jsonify
from Backend.DAOs.supplies import SuppliesDao
from Backend.DAOs.warehouse_dao import WarehouseDAO
from Backend.DAOs.user_dao import UserDAO
from Backend.DAOs.stored_in import StoredInDAO
from Backend.DAOs.racks import RackDAO



class Result(Enum):
    VALID = True
    INVALID = False


class ValidationResponse:
    """
    Simple wrapper to return useful information from the validation functions.
    """
    def __init__(self, result: Result, value: Any) -> None:
        self.result = result
        self.value = value

    def isValid(self) -> bool:
        return self.result.value
    

def ValidResponse(*values) -> ValidationResponse:
    if len(values) == 0: values = None
    elif len(values) == 1: values = values[0]
    return ValidationResponse(Result.VALID, values)

def InvalidResponse(*values) -> ValidationResponse:
    if len(values) == 0: values = None
    elif len(values) == 1: values = values[0]
    return ValidationResponse(Result.INVALID, values)


class ValidatableTransaction:
    def _validate_enough_supplier_stock(self, partID, supplierID, partAmount) -> ValidationResponse:
        """
        Checks whether there is enough stock on the given supplier.
        Returns the stock if the response is valid.
        """
        supplies_DAO = SuppliesDao()
        stock = supplies_DAO.get_stock_for_part_and_supplier(pid=partID, sid=supplierID)
        if not stock:
            return InvalidResponse(
                jsonify(Error=f"Part {partID} not supplied by supplier {supplierID}"),
                400)
        elif stock < partAmount:
            return InvalidResponse(
                jsonify(Error=f"Not enough stock ({stock}) for requested amount ({partAmount})"),
                400)
        return ValidResponse(stock)


    def _validate_enough_budget_in_warehouse(self, unitBuyPrice, partAmount, warehouseID, cost) -> ValidationResponse:
        """
        Checks whether there is enough budget in the given warehouse.
        """
        warehouse_DAO = WarehouseDAO()
        budget = warehouse_DAO.get_warehouse_budget(wid=warehouseID)
        if not budget:
            return InvalidResponse(jsonify(Error=f"Warehouse {warehouseID} not found"), 404)
        elif budget < cost:
            return InvalidResponse(jsonify(Error=
                f"Warehouse budget (${budget}) not enough to buy {partAmount} unit(s) at ${unitBuyPrice} per unit."),
                400)
        return ValidResponse()
        

    def _validate_user_in_warehouse(self, userID, warehouseID) -> ValidationResponse:
        """
        Checks whether the given user is assigned to the given warehouse.
        """
        tuple = UserDAO().getUserByID(uid=userID)
        if not tuple:
            return InvalidResponse(
                jsonify(Error=f"Internal server error: Failed to get user with id {userID}"),
                500)
        warehouse_for_user = tuple[0][6]
        if warehouse_for_user != warehouseID:
            return InvalidResponse(
                jsonify(Error=f"User ({userID}) works at warehouse {warehouse_for_user}, not {warehouseID}"),
                400)
        return ValidResponse()


    def _validate_rack_exists(self, rackID) -> ValidationResponse:
        """
        Checks whether the rack exists.
        Returns the rack capacity if the response is valid.
        """
        rack_capacity = RackDAO().get_capacity(rid=rackID)
        if not rack_capacity: return InvalidResponse(jsonify(Error=f"Rack {rackID} does not exist"), 500)
        return ValidResponse(rack_capacity)


    def _validate_rack_is_not_in_use_for_different_part(self, rackID, warehouseID, partID) -> ValidationResponse:
        """
        Checks whether the rack is being used for a different part.
        """
        stored_in_DAO = StoredInDAO()
        result = stored_in_DAO.get_entry_with_rid(rid=rackID)
        if result and not (result[0] == warehouseID and result[1] == partID):
            return InvalidResponse(
                jsonify(Error=f"Rack ({rackID}) not assigned to warehouse ({warehouseID}) and part ({partID})"),
                400)
        return ValidResponse()
    

    def _validate_amount_fits_in_rack(self, warehouseID, partID, rackID, rack_capacity, partAmount) -> ValidationResponse:
        """
        Checks whether the amount of parts fits in the rack.
        Returns the current amount in the rack if the response is valid.
        """
        stored_in_DAO = StoredInDAO()
        current_amount_in_rack = stored_in_DAO.get_quantity(wid=warehouseID, pid=partID, rid=rackID)
        rack_delta = rack_capacity - current_amount_in_rack
        if partAmount > rack_delta:
            leftover = rack_delta if rack_delta >= 0 else 0
            return InvalidResponse(
                jsonify(Error=f"Too many parts ({partAmount}). Rack ({rackID}) can hold {leftover} more parts."),
                400)
        return ValidResponse(current_amount_in_rack)
    
    
    def _validate_enough_quantity_in_warehouse(self, warehouseID, partID, rackID, partAmount) -> ValidationResponse:
        """
        Checks whether the amount of parts in the warehouse is enough.
        Returns the current amount in the warehouse if the response is valid.
        """
        available_quantity = StoredInDAO().get_quantity(wid=warehouseID, pid=partID, rid=rackID)
        if available_quantity < partAmount:
            return InvalidResponse(
                jsonify(Error=f"Not enough stock ({available_quantity}) in warehouse ({warehouseID})"),
                400)
        return ValidResponse(available_quantity)
