# servicenow_client.py
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
from httpx import HTTPError


class RequestSession:
    def __init__(self, url, auth, httpx_timeout=10):
        client = httpx.Client()
        client.auth = auth
        client.timeout = httpx_timeout
        self._base_url = url
        self._api_url = url + "/api/now/"
        self._request_sesh = client

    def _get(self, path):
        self._response = self._request_sesh.get(self._api_url + f"{path}")
        self._response.raise_for_status()
        self._response_json = self._response.json()
        return self._response_json

    def _post(self, path, payload):
        self._response = self._request_sesh.post(
            self._api_url + f"{path}", json=payload
        )
        self._response.raise_for_status()
        self._response_json = self._response.json()
        return self._response_json

    def _post_files(self, path, parameters, file):
        self._request_sesh.headers.update({"Content-Type": "image/jpeg"})
        self._response = self._request_sesh.post(
            self._api_url + f"{path}", params=parameters, data=file
        )
        self._response.raise_for_status()

    def _put(self, path, payload):
        self._response = self._request_sesh.put(self._api_url + f"{path}", data=payload)
        self._response.raise_for_status()
        self._response_json = self._response.json()
        return self._response_json

    def _patch(self, path, payload):
        self._response = self._request_sesh.patch(
            self._api_url + f"{path}", data=payload
        )
        self._response.raise_for_status()
        self._response_json = self._response.json()
        return self._response_json

    def _delete(self, path):
        self._response = self._request_sesh.delete(self._api_url + f"{path}")
        self._response.raise_for_status()

    def get_all_records(self, table_name):
        return self._get(f"table/{table_name}")

    def get_record_by_sys_id(self, table_name, sys_id):
        return self._get(f"table/{table_name}/{sys_id}")

    def insert_staging_record(self, table_name, payload):
        return self._post(f"import/{table_name}/insertMultiple", payload=payload)

    def insert_multiple_records_to_table(self, table_name, payload, max_workers=10):
        futures = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for record in payload:
                futures.append(
                    executor.submit(self._post, f"table/{table_name}", record)
                )
        responses = []
        exceptions = []
        for future in as_completed(futures):
            try:
                responses.append(future.result())
            except Exception as exc:
                exceptions.append(exc)
        return responses, exceptions


class Incidents(RequestSession):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_all(self):
        return self._get("table/incident")

    def get_by_sys_id(self, sysid):
        return self._get(f"table/incident/{sysid}")

    def add_comment_to_inc(self, sysid, comment):
        payload = dict()
        payload["comments"] = comment
        payload = json.dumps(payload)
        return self._put(f"table/incident/{sysid}", payload=payload)

    def create_inc(self, description, comments):
        payload = dict()
        payload["short_description"] = description
        payload["comments"] = comments
        payload = json.dumps(payload)
        return self._post("table/incident", payload=payload)

    def add_attachment_to_inc(self, file_path, filename, sys_id):
        with open(file_path, "rb") as fp:
            params = dict()
            params["table_name"] = "incidents"
            params["table_sys_id"] = sys_id
            params["file_name"] = filename
            return self._post_files(f"attachment/file", parameters=params, file=fp)


class CoreCompany(RequestSession):
    def __int__(self, **kwargs):
        super.__init__(**kwargs)

    def get_all(self):
        return self._get(f"table/core_company")

    def create_vendor(self, vendor_name):
        payload = dict()
        payload["name"] = vendor_name.capitalize()
        payload["manufacturer"] = True
        payload = json.dumps(payload)
        self._post("table/core_company", payload=payload)
        return self._response_json["result"]["sys_id"], vendor_name


class Location(RequestSession):
    def __int__(self, **kwargs):
        super.__init__(**kwargs)

    def get_all(self):
        return self._get(f"table/cmn_location")

    def create_location(self, location_name):
        payload = dict()
        payload["name"] = location_name.capitalize()
        payload = json.dumps(payload)
        try:
            self._post("table/cmn_location", payload=payload)
        except HTTPError:
            return Exception
        return self._response_json["result"]["sys_id"]


class CmdbCi:
    def __init__(self, sesh_dict):
        self._sesh_dict = sesh_dict

    @property
    def net_gear(self):
        return NetGear(**self._sesh_dict)


class NetGear(RequestSession):
    def get_all(self):
        return self._get(f"table/cmdb_ci_netgear")

    def create_ci(self, device_data):
        device_data = json.dumps(device_data)
        return self._post(f"table/cmdb_ci_netgear", payload=device_data)

    def update_ci(self, device_data, ci_sys_id):
        device_data = json.dumps(device_data)
        return self._patch(f"table/cmdb_ci_netgear/{ci_sys_id}", payload=device_data)

    def delete_ci(self, ci_sys_id):
        return self._delete(f"table/cmdb_ci_netgear/{ci_sys_id}")


class Snow:
    def __init__(self, auth, url, httpx_timeout=10):
        sesh_dict = dict()
        sesh_dict["auth"] = auth
        sesh_dict["url"] = url
        sesh_dict["httpx_timeout"] = httpx_timeout
        self._sesh_dict = sesh_dict

    @property
    def incidents(self):
        return Incidents(**self._sesh_dict)

    @property
    def vendors(self):
        return CoreCompany(**self._sesh_dict)

    @property
    def location(self):
        return Location(**self._sesh_dict)

    @property
    def cmdb(self):
        return CmdbCi(self._sesh_dict)

    @property
    def request_client(self):
        return RequestSession(**self._sesh_dict)
