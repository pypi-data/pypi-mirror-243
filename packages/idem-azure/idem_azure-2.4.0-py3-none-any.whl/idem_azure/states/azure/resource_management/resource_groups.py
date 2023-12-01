"""State module for managing Resource Group."""
import copy
from typing import Any
from typing import Dict


__contracts__ = ["resource"]


RESOURCE_TYPE_FULL = "azure.resource_management.resource_groups"


async def present(
    hub,
    ctx,
    name: str,
    resource_group_name: str,
    location: str,
    subscription_id: str = None,
    tags: Dict = None,
    resource_id: str = None,
) -> dict:
    r"""Create or update Resource Groups.

    Args:
        name(str): The identifier for this state.
        resource_group_name(str): The name of the resource group to create or update. Can include alphanumeric, underscore, parentheses, hyphen, period (except at end), and Unicode characters that match the allowed characters.Regex pattern: ^[-\w\._\(\)]+$.
        location(str): Resource location.
        subscription_id(str, Optional): Subscription Unique id.
        tags(dict, Optional): Resource tags.
        resource_id(str, Optional): Resource Group id on Azure.

    Returns:
        dict

    Examples:
        .. code-block:: sls

            resource_is_present:
              azure.resource_management.resource_groups.present:
                - name: value
                - resource_group_name: value
                - subscription_id: value
    """
    result = ctx.get("wrapper_result")

    if ctx.get("skip_present"):
        return result

    if not result:
        error_message = hub.tool.azure.comment_utils.no_result_from_wrapper(
            RESOURCE_TYPE_FULL, name
        )
        hub.log.error(error_message)
        return {
            "result": False,
            "old_state": None,
            "new_state": None,
            "name": name,
            "comment": [error_message],
        }

    computed = ctx.get("computed")
    computed_resource_id = computed.get("resource_id")
    computed_resource_url = computed.get("resource_url")
    existing_resource = result["old_state"]

    if not existing_resource:
        if ctx.get("test", False):
            # Return a proposed state by Idem state --test
            result["new_state"] = hub.tool.azure.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_group_name": resource_group_name,
                    "subscription_id": subscription_id,
                    "tags": tags,
                    "location": location,
                    "resource_id": computed_resource_id,
                },
            )
            result["comment"].append(
                hub.tool.azure.comment_utils.would_create_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            return result

        else:
            # PUT operation to create a resource
            payload = hub.tool.azure.resource_management.resource_groups.convert_present_to_raw_resource_group(
                location=location,
                tags=tags,
            )
            response_put = await hub.exec.request.json.put(
                ctx,
                url=computed_resource_url,
                success_codes=[200, 201],
                json=payload,
            )

        if not response_put["result"]:
            hub.log.debug(
                hub.tool.azure.comment_utils.could_not_create_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            result["comment"].extend(
                hub.tool.azure.result_utils.extract_error_comments(response_put)
            )
            result["result"] = False
            return result

        result[
            "new_state"
        ] = hub.tool.azure.resource_management.resource_groups.convert_raw_resource_group_to_present(
            resource=response_put["ret"],
            idem_resource_name=name,
            resource_group_name=resource_group_name,
            resource_id=computed_resource_id,
            subscription_id=subscription_id,
        )
        result["comment"].append(
            hub.tool.azure.comment_utils.create_comment(RESOURCE_TYPE_FULL, name)
        )
        return result
    else:
        raw_existing_resource = hub.tool.azure.resource_management.resource_groups.convert_present_to_raw_resource_group(
            location=existing_resource.get("location"),
            tags=existing_resource.get("tags"),
        )

        # Generate a new PUT operation payload with new values
        new_payload = hub.tool.azure.resource_management.resource_groups.update_resource_groups_payload(
            raw_existing_resource,
            {"tags": tags},
        )
        if ctx.get("test", False):
            if new_payload["ret"] is None:
                result["new_state"] = copy.deepcopy(result["old_state"])
                result["comment"].append(
                    hub.tool.azure.comment_utils.no_property_to_be_updated_comment(
                        "azure.resource_management.resource_groups", name
                    )
                )
            else:
                result[
                    "new_state"
                ] = hub.tool.azure.resource_management.resource_groups.convert_raw_resource_group_to_present(
                    resource=new_payload["ret"],
                    idem_resource_name=name,
                    resource_group_name=resource_group_name,
                    resource_id=computed_resource_id,
                    subscription_id=subscription_id,
                )
                result["comment"].append(
                    hub.tool.azure.comment_utils.would_update_comment(
                        RESOURCE_TYPE_FULL, name
                    )
                )
            return result
        # PUT operation to update a resource
        if new_payload["ret"] is None:
            result["new_state"] = copy.deepcopy(result["old_state"])
            result["comment"].append(
                hub.tool.azure.comment_utils.no_property_to_be_updated_comment(
                    "azure.resource_management.resource_groups", name
                )
            )
            return result
        result["comment"].extend(new_payload["comment"])
        response_put = await hub.exec.request.json.put(
            ctx,
            url=computed_resource_url,
            success_codes=[200, 201],
            json=new_payload["ret"],
        )

        if not response_put["result"]:
            hub.log.debug(
                hub.tool.azure.comment_utils.could_not_update_comment(
                    RESOURCE_TYPE_FULL, name
                )
            )
            result["result"] = False
            result["comment"].extend(
                hub.tool.azure.result_utils.extract_error_comments(response_put)
            )
            return result

        result[
            "new_state"
        ] = hub.tool.azure.resource_management.resource_groups.convert_raw_resource_group_to_present(
            resource=response_put["ret"],
            idem_resource_name=name,
            resource_group_name=resource_group_name,
            resource_id=computed_resource_id,
            subscription_id=subscription_id,
        )
        result["comment"].append(
            hub.tool.azure.comment_utils.update_comment(RESOURCE_TYPE_FULL, name)
        )
        return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    resource_group_name: str = None,
    subscription_id: str = None,
) -> dict:
    r"""Delete Resource Groups.

    Args:
        name(str): The identifier for this state.
        resource_id(str, Optional): Resource Group resource id in Azure.
        resource_group_name(str, Optional): The name of the resource group to delete. The name is case insensitive.Regex pattern: ^[-\w\._\(\)]+$.
        subscription_id(str, Optional): Subscription Unique id.

    Returns:
        dict

    Examples:
        .. code-block:: sls

            resource_is_absent:
              azure.resource_management.resource_groups.absent:
                - name: value
                - resource_group_name: value
                - subscription_id: value
    """
    return hub.tool.azure.result_utils.absent_implemented_through_wrapper_result(
        "azure.resource_management.resource_groups", name
    )


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Lists all Resource Groups under the same subscription.


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe azure.resource_management.resource_groups
    """
    result = {}
    ret_list = await hub.exec.azure.resource_management.resource_groups.list(ctx)
    if not ret_list["ret"]:
        hub.log.debug(f"Could not describe resource_groups {ret_list['comment']}")
        return result

    for resource in ret_list["ret"]:
        resource_id = resource["resource_id"]
        result[resource_id] = {
            "azure.resource_management.resource_groups.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result


def is_pending(hub, ret: dict, state: str = None, **pending_kwargs) -> bool:
    """Default implemented for each module."""
    return hub.tool.azure.resource_utils.is_pending(
        ret=ret, state=state, **pending_kwargs
    )
