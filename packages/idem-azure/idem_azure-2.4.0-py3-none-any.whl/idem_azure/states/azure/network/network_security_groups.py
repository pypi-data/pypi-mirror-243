"""State module for managing Network security group."""
import copy
import uuid
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_group_name: str,
    network_security_group_name: str,
    location: str,
    security_rules: List[
        make_dataclass(
            "SecurityRule",
            [
                ("name", str),
                ("priority", int),
                ("direction", str),
                ("access", str),
                ("protocol", str),
                ("source_port_range", str, field(default=None)),
                ("destination_port_range", str, field(default=None)),
                ("source_address_prefix", str, field(default=None)),
                ("destination_address_prefix", str, field(default=None)),
                ("source_port_ranges", List[str], field(default=None)),
                ("destination_port_ranges", List[str], field(default=None)),
                ("source_address_prefixes", List[str], field(default=None)),
                ("destination_address_prefixes", List[str], field(default=None)),
            ],
        )
    ] = None,
    tags: Dict = None,
    subscription_id: str = None,
    resource_id: str = None,
) -> Dict:
    r"""Create or update Network Security Groups.

    Args:
        name(str): The identifier for this state.
        resource_group_name(str): The name of the resource group.
        network_security_group_name(str): The name of the network security group.
        location(str): The location to create the resource in.
        security_rules(list[dict[str, Any]], Optional): List of security rules. Each security rule contains:

            * name(str):
                The name of the security rule.
            * priority(int):
                The priority of the security rule. The value can be between 100 and 4096.The priority number must
                be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
            * direction(str):
                The direction of the rule. The direction specifies if rule will be evaluated on incoming or outgoing traffic.
            * access(str):
                The network traffic is allowed or denied.
            * protocol(str):
                Network protocol this rule applies to.
            * source_port_range(str, Optional):
                The source port or range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
            * destination_port_range(str, Optional):
                The destination port or range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
            * source_address_prefix(str, Optional):
                The source address prefix. CIDR or source IP range. Asterisk '*' can also be used to match all
                source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. If
                this is an ingress rule, specifies where network traffic originates from.
            * destination_address_prefix(str, Optional):
                The destination address prefix. CIDR or destination IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork',
                'AzureLoadBalancer' and 'Internet' can also be used.
            * source_port_ranges(list[str], Optional):
                The source port ranges. Either this or source_port_range need to be provided.
            * destination_port_ranges(list[str], Optional):
                The destination port ranges.Either this or destination_port_range need to be provided.
            * source_address_prefixes(list[str], Optional):
                The CIDR or source IP ranges. Either source_address_prefix or source_address_prefixes needs to be provided.
            * destination_address_prefixes(list[str], Optional):
                The destination address prefixes. CIDR or destination IP ranges. Either destination_address_prefix or destination_address_prefixes needs to be provided.
        tags(Dict, Optional): Resource tags.
        subscription_id(str, Optional): Subscription Unique id.
        resource_id(str, Optional): Resource Group id on Azure.

    Returns:
        Dict

    Examples:
        .. code-block:: sls

            resource_is_present:
              azure.network.network_security_groups.present:
                - name: value
                - resource_group_name: value
                - network_security_group_name: value
                - location: value
                - tags: value
    """
    result = ctx.get("wrapper_result")

    if ctx.get("skip_present"):
        return result

    if not result:
        error_message = hub.tool.azure.comment_utils.no_result_from_wrapper(
            "azure.network.network_security_groups", name
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
                    "network_security_group_name": network_security_group_name,
                    "subscription_id": subscription_id,
                    "security_rules": security_rules,
                    "tags": tags,
                    "location": location,
                    "resource_id": computed_resource_id,
                },
            )
            result["comment"].append(
                f"Would create azure.network.network_security_groups '{name}'"
            )
            return result

        else:
            # PUT operation to create a resource
            payload = hub.tool.azure.network.network_security_groups.convert_present_to_raw_network_security_groups(
                location=location,
                security_rules=security_rules,
                tags=tags,
            )
            response_put = await hub.exec.request.json.put(
                ctx,
                url=computed_resource_url,
                success_codes=[200, 201],
                json=payload,
            )

            if response_put["status"] == 202:
                result["rerun_data"] = {
                    "operation_id": str(uuid.uuid4()),
                    "operation_headers": dict(response_put.get("headers")),
                    "resource_id": f"{computed_resource_id}",
                    "resource_url": f"{computed_resource_url}",
                    "old_state": result["old_state"],
                }
                return result
            elif not response_put["result"] and response_put["status"] != 202:
                hub.log.debug(
                    f"Could not create azure.network.network_security_groups {response_put['comment']} {response_put['ret']}"
                )
                result["comment"].extend(
                    hub.tool.azure.result_utils.extract_error_comments(response_put)
                )
                result["result"] = False
                return result
            else:
                result[
                    "new_state"
                ] = hub.tool.azure.network.network_security_groups.convert_raw_network_security_groups_to_present(
                    resource=response_put["ret"],
                    idem_resource_name=name,
                    resource_id=computed_resource_id,
                    network_security_group_name=network_security_group_name,
                    resource_group_name=resource_group_name,
                    subscription_id=subscription_id,
                )

            result["comment"].append(
                f"Created azure.network.network_security_groups '{name}'"
            )
            return result
    else:
        raw_existing_resource = hub.tool.azure.network.network_security_groups.convert_present_to_raw_network_security_groups(
            location=existing_resource.get("location"),
            security_rules=existing_resource.get("security_rules"),
            tags=existing_resource.get("tags"),
        )
        # Generate a new PUT operation payload with new values to update
        new_payload = hub.tool.azure.network.network_security_groups.update_network_security_groups_payload(
            raw_existing_resource,
            {"tags": tags, "security_rules": security_rules},
        )

        if ctx.get("test", False):
            if new_payload["ret"] is None:
                result["new_state"] = copy.deepcopy(result["old_state"])
                result["comment"].append(
                    hub.tool.azure.comment_utils.no_property_to_be_updated_comment(
                        "azure.network.network_security_groups", name
                    )
                )
            else:
                result[
                    "new_state"
                ] = hub.tool.azure.network.network_security_groups.convert_raw_network_security_groups_to_present(
                    resource=new_payload["ret"],
                    idem_resource_name=name,
                    resource_id=computed_resource_id,
                    network_security_group_name=network_security_group_name,
                    resource_group_name=resource_group_name,
                    subscription_id=subscription_id,
                )
                result["comment"].append(
                    f"Would update azure.network.network_security_groups '{name}'"
                )
            return result

        # PUT call to update the resource
        if new_payload["ret"] is None:
            result["new_state"] = copy.deepcopy(result["old_state"])
            result["comment"].append(
                hub.tool.azure.comment_utils.no_property_to_be_updated_comment(
                    "azure.network.network_security_groups", name
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

        if response_put["status"] == 202:
            result["rerun_data"] = {
                "operation_id": str(uuid.uuid4()),
                "operation_headers": dict(response_put.get("headers")),
                "resource_id": f"{computed_resource_id}",
                "resource_url": f"{computed_resource_url}",
                "old_state": result["old_state"],
            }
            return result
        elif not response_put["result"] and response_put["status"] != 202:
            hub.log.debug(
                f"Could not update azure.network.network_security_groups {response_put['comment']} {response_put['ret']}"
            )
            result["result"] = False
            result["comment"].extend(
                hub.tool.azure.result_utils.extract_error_comments(response_put)
            )
            return result

        result[
            "new_state"
        ] = hub.tool.azure.network.network_security_groups.convert_raw_network_security_groups_to_present(
            resource=response_put["ret"],
            idem_resource_name=name,
            resource_id=computed_resource_id,
            network_security_group_name=network_security_group_name,
            resource_group_name=resource_group_name,
            subscription_id=subscription_id,
        )
        if result["old_state"] == result["new_state"]:
            result["comment"].append(
                hub.tool.azure.comment_utils.no_property_to_be_updated_comment(
                    "azure.network.network_security_groups", name
                )
            )
            return result

        result["comment"].append(
            f"Updated azure.network.network_security_groups '{name}'"
        )
        return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    resource_group_name: str = None,
    network_security_group_name: str = None,
    subscription_id: str = None,
) -> Dict:
    r"""Delete Network Security Groups.

    Args:
        name(str): The identifier for this state.
        resource_id(str, Optional): Resource Group id on Azure.
        resource_group_name(str, Optional): The name of the resource group.
        network_security_group_name(str, Optional): The name of the network security group.
        subscription_id(str, Optional): Unique subscription ID

    Returns:
        Dict

    Examples:
        .. code-block:: sls

            resource_is_absent:
              azure.network.network_security_groups.absent:
                - name: value
                - resource_group_name: value
                - network_security_group_name: value
    """
    return hub.tool.azure.result_utils.absent_implemented_through_wrapper_result(
        "azure.network.network_security_groups", name
    )


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""Describe the resource in a way that can be recreated/managed with the corresponding "present" function.
    Lists all Network Security Groups under the same subscription.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe azure.network.network_security_groups
    """
    result = {}
    ret = await hub.exec.azure.network.network_security_groups.list(ctx)
    if not ret["result"]:
        hub.log.debug(f"Could not describe network_security_groups {ret['comment']}")
        return {}

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            f"azure.network.network_security_groups.present": [
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
