import uuid
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub, ctx, exec_mod_ref: str, resource_id: str, *, name: str, **kwargs
) -> Dict[str, Any]:
    func = hub.exec[exec_mod_ref].get

    if "name" in func.signature._parameters:
        kwargs["name"] = name

    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    return result


async def list_(
    hub, ctx, exec_mod_ref: str, resource_id: str = None, *, name: str = None, **kwargs
) -> Dict[str, Any]:
    func = hub.exec[exec_mod_ref].list

    if "name" in func.signature._parameters:
        kwargs["name"] = name
    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    # Ensure every resource has a resource_id
    acc = []
    for resource in result["ret"]:
        resource_id = (
            resource.get("resource_id") or f"{resource.get('name')}-{uuid.uuid4()}"
        )
        acc.append(resource)

    result["ret"] = acc
    return result


async def create(
    hub, ctx, exec_mod_ref: str, resource_id: str = None, *, name: str = None, **kwargs
) -> Dict[str, Any]:
    func = hub.exec[exec_mod_ref].create

    if "name" in func.signature._parameters:
        kwargs["name"] = name
    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    return result


async def update(
    hub, ctx, exec_mod_ref: str, resource_id: str = None, *, name: str = None, **kwargs
) -> Dict[str, Any]:
    func = hub.exec[exec_mod_ref].update

    if "name" in func.signature._parameters:
        kwargs["name"] = name
    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    return result


async def delete(
    hub, ctx, exec_mod_ref: str, resource_id: str = None, *, name: str = None, **kwargs
) -> Dict[str, Any]:
    func = hub.exec[exec_mod_ref].delete

    if "name" in func.signature._parameters:
        kwargs["name"] = name
    if "resource_id" in func.signature._parameters:
        kwargs["resource_id"] = resource_id

    coro = func(ctx, **kwargs)
    result = await hub.pop.loop.unwrap(coro)

    return result
