import logging

from nagra_panorama_api.restapi import PanoramaClient

# API_KEY = os.environ["PANOS_API_KEY"]
# PANORAMA = os.environ["PANOS_HOSTNAME"]

log = logging.getLogger("Rules Getter")


def get_security_rules(host, api_key, device_goup):
    """
    Function to get all security rules in Panorama
    """
    client = PanoramaClient(host, api_key)

    payload = {
        "device-group": device_goup,
    }
    security_post_rules = client.policies.SecurityPostRules.get(params=payload)
    security_pre_rules = client.policies.SecurityPreRules.get(params=payload)
    if not security_post_rules:
        log.warning(f"Device group {device_goup} has no Security Post Rules")
    if not security_pre_rules:
        log.warning(f"Device group {device_goup} has no Security Pre Rules")
    return [*security_post_rules, *security_pre_rules]


def get_nat_rules(host, api_key, device_goup):
    """
    Function to get all NAT rules in Panorama
    """
    client = PanoramaClient(host, api_key)

    payload = {
        "device-group": device_goup,
    }
    nat_post_rules = client.policies.NatPostRules.get(params=payload)
    nat_pre_rules = client.policies.NatPreRules.get(params=payload)
    return [*nat_post_rules, *nat_pre_rules]


def get_pbf_rules(host, api_key, device_goup):
    """
    Function to get all PBF rules in Panorama
    """
    client = PanoramaClient(host, api_key)

    payload = {
        "device-group": device_goup,
    }
    pbf_post_rules = client.policies.PolicyBasedForwardingPostRules.get(params=payload)
    pbf_pre_rules = client.policies.PolicyBasedForwardingPreRules.get(params=payload)
    return [*pbf_post_rules, *pbf_pre_rules]
