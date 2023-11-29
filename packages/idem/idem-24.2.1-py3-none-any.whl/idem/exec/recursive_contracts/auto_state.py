"""
If an exec module plugin implements this contract,
the same ref can be used to call the state functions "present", "absent", and "describe".
"""
from typing import Any
from typing import Dict


def sig_get(hub, ctx, resource_id: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Searches for a resource with the given resource_id.
    If it exists, it returns a dictionary with the resource's attributes
    normalized to the format of the "create" function parameters.
    If the resource does not exist, returns None.
    """
    return {"result": True | False, "comment": [], "ret": {} | None}


def sig_list(hub, ctx, **kwargs) -> Dict[str, Any]:
    """
    Returns a dictionary mapping resource_id's to dictionary of each
    resource's attributes normalized to the format of the "create" function parameters.
    """
    return {"result": True | False, "comment": [], "ret": {str: []}}


def sig_create(hub, ctx, *args, **kwargs) -> Dict[str, Any]:
    """
    Creates a resource and returns its attributes.
    The signature of this function is used for "present" state documentation
    and for validation of resource parameters in many other places.
    """
    return {"result": True | False, "comment": [], "ret": {}}


def sig_update(hub, ctx, resource_id: str, *args, **kwargs) -> Dict[str, Any]:
    """
    The resource's "before" state is contained in ctx.before.
    The desired state for the resource are represented in "kwargs".
    """
    return {"result": True | False, "comment": [], "ret": {}}


def sig_delete(hub, ctx, resource_id: str, *args, **kwargs) -> Dict[str, Any]:
    """
    Delete the resource with the given resource_id.
    Any kwargs that are required or that differ from the "create" options should be documented here explicitly
    """
    return {"result": True | False, "comment": [], "ret": {}}
