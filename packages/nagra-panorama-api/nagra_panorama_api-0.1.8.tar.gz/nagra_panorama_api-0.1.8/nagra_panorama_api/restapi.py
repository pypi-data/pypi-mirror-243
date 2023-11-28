import json
import logging
from itertools import chain

import requests

# Remove warning for unverified certificate
# https://stackoverflow.com/questions/27981545/suppress-insecurerequestwarning-unverified-https-request-is-being-made-in-pytho
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from .rest_resources import (
    PanoramaDevicesResourceType,
    PanoramaNetworkResourceType,
    PanoramaObjectsResourceType,
    PanoramaPanoramaResourceType,
    PanoramaPoliciesResourceType,
)

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

log = logging.getLogger(__name__)

# https://docs.paloaltonetworks.com/pan-os/9-1/pan-os-panorama-api/get-started-with-the-pan-os-rest-api/pan-os-rest-api-error-codes
PANORAMA_ERRORS = {
    1: ("The operation was canceled, typically by the caller."),
    2: ("Unknown internal server error."),
    3: ("Bad request. The caller specified an invalid parameter."),
    4: (
        "Gateway timeout. A firewall or Panorama module timed out "
        "before a backend operation completed."
    ),
    5: ("Not found. The requested entity was not found."),
    6: ("Conflict. The entity that the caller attempted to create already exists."),
    7: (
        "Forbidden. The caller does not have permission "
        "to execute the specified operation."
    ),
    8: ("Resource exhausted. Some resource has been exhausted."),
    9: (
        "Failed precondition. The operation was rejected because "
        "the system is not in a state required "
        "for the execution of the operation."
    ),
    10: ("Aborted because of conflict. A typical cause is a concurrency issue."),
    11: (
        "Out of range. The operation was attempted past a valid range. "
        "And example is reaching an end-of-file."
    ),
    12: (
        "Not implemented. The operation is disabled, not implemented, "
        "or not supported."
    ),
    13: (
        "Internal server error. An unexpected and potentially serious "
        "internal error occurred."
    ),
    14: ("Service unavailable. The service is temporarily unavailable."),
    15: ("Internal server error. Unrecoverable data loss or data corruption occurred."),
    16: (
        "Unauthorized. The request does not have "
        "valid authentication credentials to perform the operation."
    ),
}
SUCCESS_CODE = 19

OBJECT_RESOURCES = [
    "Addresses",
    "AddressGroups",
    "Regions",
    "Applications",
    "ApplicationGroups",
    "ApplicationFilters",
    "Services",
    "ServiceGroups",
    "Tags",
    "GlobalProtectHIPObjects",
    "GlobalProtectHIPProfiles",
    "ExternalDynamicLists",
    "CustomDataPatterns",
    "CustomSpywareSignatures",
    "CustomVulnerabilitySignatures",
    "CustomURLCategories",
    "AntivirusSecurityProfiles",
    "AntiSpywareSecurityProfiles",
    "VulnerabilityProtectionSecurityProfiles",
    "URLFilteringSecurityProfiles",
    "FileBlockingSecurityProfiles",
    "WildFireAnalysisSecurityProfiles",
    "DataFilteringSecurityProfiles",
    "DoSProtectionSecurityProfiles",
    "SecurityProfileGroups",
    "LogForwardingProfiles",
    "AuthenticationEnforcements",
    "DecryptionProfiles",
    "DecryptionForwardingProfiles",
    "Schedules",
    "SDWANPathQualityProfiles",
    "SDWANTrafficDistributionProfiles",
]

POLICY_RESOURCES = [
    "SecurityRules",
    "NATRules",
    "QoSRules",
    "PolicyBasedForwardingRules",
    "DecryptionRules",
    "TunnelInspectionRules",
    "ApplicationOverrideRules",
    "AuthenticationRules",
    "DoSRules",
    "SDWANRules",
]

NETWORK_RESOURCES = [
    "EthernetInterfaces",
    "AggregateEthernetInterfaces",
    "VLANInterfaces",
    "LoopbackInterfaces",
    "TunnelIntefaces",
    "SDWANInterfaces",
    "Zones",
    "VLANs",
    "VirtualWires",
    "VirtualRouters",
    "IPSecTunnels",
    "GRETunnels",
    "DHCPServers",
    "DHCPRelays",
    "DNSProxies",
    "GlobalProtectPortals",
    "GlobalProtectGateways",
    "GlobalProtectGatewayAgentTunnels",
    "GlobalProtectGatewaySatelliteTunnels",
    "GlobalProtectGatewayMDMServers",
    "GlobalProtectClientlessApps",
    "GlobalProtectClientlessAppGroups",
    "QoSInterfaces",
    "LLDP",
    "GlobalProtectIPSecCryptoNetworkProfiles",
    "IKEGatewayNetworkProfiles",
    "IKECryptoNetworkProfiles",
    "MonitorNetworkProfiles",
    "InterfaceManagementNetworkProfiles",
    "ZoneProtectionNetworkProfiles",
    "QoSNetworkProfiles",
    "LLDPNetworkProfiles",
    "SDWANInterfaceProfiles",
]

DEVICE_RESOURCES = [
    "VirtualSystems",
]

DEFAULT_PARAMS = {
    "output-format": "json",
}


class PanoramaAPI:
    def __init__(self, api_key=None, verbose=False, verify=False):
        self._verbose = verbose
        self._verify = verify
        self._api_key = api_key

    def _inner_request(
        self,
        method,
        url,
        params=None,
        headers=None,
        data=None,
        verify=None,
    ):
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if verify is None:
            verify = self._verify
        default_headers = {
            "X-PAN-KEY": self._api_key,
            # 'Accept': 'application/json, application/xml',
            # 'Content-Type': 'application/json'
        }
        headers = {**default_headers, **headers}
        params = {**DEFAULT_PARAMS, **params}
        res = requests.request(
            method,
            url,
            params=params,
            headers=headers,
            verify=verify,
        )
        # The API always returns a json, no matter what
        # if not res.ok:
        #     return None
        try:
            data = res.json()
            code = int(
                data.get("@code") or data.get("code") or SUCCESS_CODE,
            )  # Sometimes, the code is a string, some other times it is a int
            error_occured = (
                not res.ok
                or data.get("@status", "") != "success"
                # In case of success, the value 19 is used
                or code < SUCCESS_CODE
            )
            if not error_occured:
                return data, None
            message = (
                data.get("message")
                or PANORAMA_ERRORS.get(data["@code"])
                or "Something happened: " + json.dumps(data)
            )
            error = f"(CODE: {code}) {message}"
            if self._verbose:
                causes = list(
                    chain(
                        *(
                            details.get("causes", {})
                            for details in data.get("details", [])
                        ),
                    ),
                )
                details = "".join(c.get("description") for c in causes)
                error = f"{error} {details}"
            return data, error
        except Exception as e:
            return None, str(e)

    def _request(
        self,
        method,
        url,
        params=None,
        headers=None,
        data=None,
        verify=None,
        no_exception=False,
    ):
        data, error = (
            self._inner_request(
                method,
                url,
                params=params,
                headers=headers,
                data=data,
                verify=verify,
            )
            or {}
        )
        if error:
            if no_exception:
                log.error(f"Could not {method.lower()} {url}: {error}")
                return data, error
            raise Exception(error)
        data = data.get("result", {}).get("entry") or []
        return data, error

    def request(self, method, url, params=None, headers=None, data=None, verify=None):
        data, _ = (
            self._request(
                method,
                url,
                params=params,
                headers=headers,
                data=data,
                verify=verify,
            )
            or {}
        )
        return data

    def get(self, url, params=None, headers=None, data=None, verify=None):
        data, _ = (
            self._request(
                "GET",
                url,
                params=params,
                headers=headers,
                data=data,
                verify=verify,
            )
            or {}
        )
        return data
        # return data.get("result", {}).get("entry") or []

    def delete(self, url, params=None, headers=None, data=None, verify=None):
        data, _ = (
            self._request(
                "DELETE",
                url,
                params=params,
                headers=headers,
                data=data,
                verify=verify,
            )
            or {}
        )
        return data


class PanoramaClient:
    def __init__(
        self,
        domain,
        api_key=None,
        version="v10.1",
        verify=False,
        verbose=False,
    ):
        client = PanoramaAPI(api_key=api_key, verbose=verbose, verify=verify)
        self.client = client
        self.objects = PanoramaObjectsResourceType(client, domain, version=version)
        self.policies = PanoramaPoliciesResourceType(client, domain, version=version)
        self.network = PanoramaNetworkResourceType(client, domain, version=version)
        self.device = PanoramaDevicesResourceType(client, domain, version=version)
        self.panorama = PanoramaPanoramaResourceType(client, domain, version=version)
