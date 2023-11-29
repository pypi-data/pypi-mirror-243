import json
from typing import Literal, Union

from ipfabric_snow.apps.env_setup import ensure_environment_is_setup, get_auth
from ipfabric_snow.utils.servicenow_client import Snow

DATA_MAPPING_DICT = {
    "hostname": "name",
    "snHw": "serial_number",
    "loginIp": "ip_address",
    "vendor": "manufacturer",
    "version": "firmware_version",
    "siteName": "location",
    "sn": "asset_tag",
}


class ETLUtility:
    def __init__(
            self,
            ipf_data,
            snow_data,
            data_source: Union[Literal["IPF", "SNOW"], str],
            verbose=False,
    ):
        env_vars = ensure_environment_is_setup()
        auth = get_auth(env_vars)
        self.data_source = data_source
        self.ipf_data = ipf_data
        self.snow_data = snow_data
        self.diff_order = tuple()
        self.snow_model = Snow(auth=auth, url=env_vars["SNOW_URL"])
        self.vendor_cache_all = self.snow_model.vendors.get_all()["result"]
        self.location_cache_all = self.snow_model.location.get_all()["result"]
        self.vendor_cache_dict = {
            vendor["sys_id"]: vendor["name"] for vendor in self.vendor_cache_all
        }
        self.location_cache_dict = {
            location["sys_id"]: location["name"] for location in self.location_cache_all
        }
        self.mapping_dict = DATA_MAPPING_DICT
        self.verbose = verbose

    def transform_ipfabric_to_servicenow(self, ipf_data_list, mapping_dict=None):
        if not mapping_dict:
            mapping_dict = self.mapping_dict
        transformed_data_list = [
            {mapping_dict[key]: data[key] for key in mapping_dict if key in data}
            for data in ipf_data_list
        ]
        return transformed_data_list

    def transform_servicenow_to_ipfabric(self, sn_data_list, mapping_dict=None):
        if not mapping_dict:
            mapping_dict = self.mapping_dict
        reversed_mapping = {v: k for k, v in mapping_dict.items()}
        transformed_data_list = [
            self.process_vendor_and_location(
                {
                    reversed_mapping[key]: data[key]
                    for key in reversed_mapping
                    if key in data
                }
            )
            for data in sn_data_list
        ]
        return transformed_data_list

    def filter_ipf_keys(self, ipf_data):
        return {key: ipf_data[key] for key in self.mapping_dict if key in ipf_data}

    def filter_snow_keys(self, snow_data):
        reversed_mapping = {v: k for k, v in self.mapping_dict.items()}
        filtered_data = {
            key: snow_data[key] for key in reversed_mapping if key in snow_data
        }
        return self.process_vendor_and_location(filtered_data)

    def process_vendor_and_location(self, data):
        def update_data_from_cache(data_dict, key, cache, to_lower=False):
            if (
                    key in data_dict
                    and isinstance(data_dict[key], dict)
                    and "value" in data_dict[key]
            ):
                sys_id = data_dict[key]["value"]
                cached_name = cache.get(sys_id)
                if cached_name:
                    data_dict[key] = cached_name.lower() if to_lower else cached_name
                else:
                    data_dict[key] = sys_id

        update_data_from_cache(data, "vendor", self.vendor_cache_dict, to_lower=True)
        update_data_from_cache(data, "siteName", self.location_cache_dict)
        update_data_from_cache(
            data, "manufacturer", self.vendor_cache_dict, to_lower=True
        )
        update_data_from_cache(data, "location", self.location_cache_dict)

        return data

    def transform_data(self, transform_source=None):
        if not transform_source:
            transform_source = self.data_source
        if transform_source == "IPF":
            self.ipf_data = [self.filter_ipf_keys(data) for data in self.ipf_data]
            self.snow_data = self.transform_servicenow_to_ipfabric(self.snow_data)
        elif transform_source == "SNOW":
            self.snow_data = [self.filter_snow_keys(data) for data in self.snow_data]
            self.ipf_data = self.transform_ipfabric_to_servicenow(self.ipf_data)
        else:
            raise ValueError(
                f"Invalid transform_source value: {transform_source}. Expected 'IPF' or 'SNOW'."
            )

    def compute_diff(self):
        return_dict = {
            "devices_in_ipf_not_in_snow": [],
            "devices_in_snow_not_in_ipf": [],
            "changed": [],
        }

        ipf_map = {
            item.get("asset_tag") or item.get("sn"): item for item in self.ipf_data
        }
        snow_map = {
            item.get("asset_tag") or item.get("sn"): item for item in self.snow_data
        }
        added = [ipf_map[key] for key in ipf_map if key not in snow_map]
        removed = [snow_map[key] for key in snow_map if key not in ipf_map]
        for unique_key, ipf_item in ipf_map.items():
            if unique_key in snow_map:
                snow_item = snow_map[unique_key]
                if ipf_item.get("asset_tag") == snow_item.get(
                        "asset_tag"
                ) or ipf_item.get("sn") == snow_item.get("sn"):
                    differences = {
                        k: v for k, v in ipf_item.items() if v != snow_item.get(k)
                    }
                    if differences:
                        change_details = {"from": snow_item, "to": ipf_item}
                        if self.verbose:
                            change_details["details"] = [
                                {
                                    "field": key,
                                    "old_value": snow_item.get(key),
                                    "new_value": ipf_item.get(key),
                                }
                                for key in differences
                            ]
                        return_dict["changed"].append(change_details)
        return_dict["devices_in_ipf_not_in_snow"] = added
        return_dict["devices_in_snow_not_in_ipf"] = removed
        return return_dict

    @staticmethod
    def write_diff_to_file(diff: dict, file_path):
        with open(file_path, "w") as file:
            json.dump(diff, file, indent=4)
