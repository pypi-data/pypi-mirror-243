import json
import logging

import requests
import xmltodict

DEFAULT_TRUNCATION = 1000
DEFAULT_SCAN_RESULT_OUTPUT_FORMAT = "json_extended"
DEFAULT_SCAN_RESULT_MODE = "extended"
ATTRIBUTES_LIST = "ALL"  # Show attributes for each asset group along with
# the ID. Specify ALL or a comm-separated list of attribute
# names. Attribute names: ID, TITLE, OWNER_USER_NAME,
# OWNER_USER_ID, OWNER_UNIT_ID, NETWORK_IDS,
# LAST_UPDATE, IP_SET, APPLIANCE_LIST, DOMAIN_LIST,
# DNS_LIST, NETBIOS_LIST, EC2_ID_LIST, asset_group_IDS,
# ASSIGNED_USER_IDS, ASSIGNED_UNIT_IDS,
# BUSINESS_IMPACT, CVSS, COMMENTS.


_LOGGER = logging.getLogger(__name__)

# TODO: Documentation
# TODO: kwargs?


class Client:
    def __init__(self, user, password, url):
        """Creates a bibt.qualys.Client object, which may be used to
        make Qualys API calls using the same set of credentials.

        :param str user: The Qualys username with which to authenticate.
        :param str password: The password for the provided account username.
        :param str url: The root domain for Qualys, e.g.
            ``"https://qualysapi.qg1.apps.qualys.com"``.
        """
        self.session = requests.Session()
        self.session.auth = (user, password)
        self.session.headers.update(
            {
                "X-Requested-With": "Python.requests",
                "Content-Type": "text/xml",
                "Cache-Control": "no-cache",
            }
        )
        self.url = url

    def close(self):
        """Cleanly closes the HTTP session with Qualys and sets
        ``self.session`` to ``None`` (making this Client unusable).
        """
        self.session.close()
        self.session = None

    def _handle_request(self, request):
        try:
            request.raise_for_status()
        except Exception:
            _LOGGER.error(f"Status: [{request.status_code}] {request.text}")
            raise

        _LOGGER.debug(f"Status: [{request.status_code}]")
        return request

    def _make_list_request(
        self,
        endpoint,
        key,
        params={},
        force_list=None,
        limit=0,
    ):
        if not self.session:
            raise Exception(
                "Cannot make requests via a closed HTTP session! "
                "Please create a new Client object to initialize a new session."
            )
        request_url = self.url + endpoint
        params["action"] = "list"
        full_resp = []
        while request_url:
            _LOGGER.debug(f"Request URL: {request_url}")
            _LOGGER.debug(f"Request params: {params}")
            resp = self._handle_request(self.session.get(request_url, params=params))
            resp_json = xmltodict.parse(
                resp.text,
                attr_prefix="",
                cdata_key="text",
                comment_key="comment",
                force_list=force_list,
            )

            # handle special case of final key being different
            final_key = key
            if key == "SCHEDULE_SCAN":
                final_key = "SCAN"

            resp_json_data = resp_json[f"{key}_LIST_OUTPUT"]["RESPONSE"][f"{key}_LIST"][
                final_key
            ]
            _LOGGER.debug(f"Extending list of type {key} by {len(resp_json_data)}...")
            full_resp.extend(resp_json_data)
            try:
                params = None
                request_url = resp_json[f"{key}_LIST_OUTPUT"]["RESPONSE"]["WARNING"][
                    "URL"
                ]
            except KeyError:
                request_url = None
        return full_resp

    def _make_delete_request(self, endpoint, id):
        if not self.session:
            raise Exception(
                "Cannot make requests via a closed HTTP session! "
                "Please create a new Client object to initialize a new session."
            )

        resp = self._handle_request(
            self.session.post(
                self.url + endpoint, params={"action": "delete", "id": id}
            )
        )
        return resp

    def list_asset_groups(
        self,
        truncation_limit=DEFAULT_TRUNCATION,
        show_attributes=ATTRIBUTES_LIST,
        asset_group_title=None,
        force_list=["IP", "IP_RANGE", "DOMAIN_LIST", "DNS"],
        clean_data=True,
    ):
        _LOGGER.info("Requesting asset group data from Qualys...")
        _LOGGER.debug(
            f"Args: force_list={force_list} clean_data=[{clean_data}] "
            f"asset_group_title=[{asset_group_title}] "
            f"truncation_limit=[{truncation_limit}] show_attributes=[{show_attributes}]"
        )
        params = {
            "truncation_limit": truncation_limit,
            "show_attributes": show_attributes,
        }
        if asset_group_title:
            params["title"] = asset_group_title
        resp = self._make_list_request(
            "/api/2.0/fo/asset/group/",
            "ASSET_GROUP",
            params=params,
            force_list=force_list,
        )
        if clean_data:
            _LOGGER.info("Cleaning data...")
            for i in range(len(resp)):
                # Instead of a string of CSV, seperate into a list of values
                if "HOST_IDS" in resp[i]:
                    resp[i]["HOST_IDS"] = resp[i]["HOST_IDS"].split(", ")
                # Instead of a string of CSV, seperate into a list of values
                if "ASSIGNED_USER_IDS" in resp[i]:
                    resp[i]["ASSIGNED_USER_IDS"] = resp[i]["ASSIGNED_USER_IDS"].split(
                        ", "
                    )
                # Ensure each domain list is a string, rather than an non-standard dict
                if "DOMAIN_LIST" in resp[i]:
                    for j in range(len(resp[i]["DOMAIN_LIST"])):
                        if isinstance(resp[i]["DOMAIN_LIST"][j]["DOMAIN"], dict):
                            resp[i]["DOMAIN_LIST"][j]["DOMAIN"] = json.dumps(
                                resp[i]["DOMAIN_LIST"][j]["DOMAIN"]
                            )

        _LOGGER.info(f"Returning data for {len(resp)} asset groups...")
        return resp

    def list_hosts(
        self,
        truncation_limit=DEFAULT_TRUNCATION,
        show_attributes=ATTRIBUTES_LIST,
        force_list=None,
    ):
        _LOGGER.info("Requesting asset group data from Qualys...")
        _LOGGER.debug(
            f"Args: force_list={force_list} "
            f"truncation_limit=[{truncation_limit}] show_attributes=[{show_attributes}]"
        )
        resp = self._make_list_request(
            "/api/2.0/fo/asset/host/",
            "HOST",
            params={
                "truncation_limit": truncation_limit,
                "show_attributes": show_attributes,
            },
            force_list=force_list,
        )

        _LOGGER.info(f"Returning data for {len(resp)} hosts...")
        return resp

    def list_scan_schedules(self, force_list=["ASSET_GROUP_TITLE"]):
        """List all configured scan schedules in Qualys.

        :param list force_list: A list of keys to force into list format when parsing
            the returned XML into lists and dictionaries.
            Defaults to ``["ASSET_GROUP_TITLE"]``.
        :return list: A list of dicts, containing metadata for all scan schedules.
        """
        _LOGGER.info("Requesting scan schedule data from Qualys...")
        _LOGGER.debug(f"Args: force_list=[{force_list}]")
        scan_schedules = self._make_list_request(
            "/api/2.0/fo/schedule/scan/",
            "SCHEDULE_SCAN",
            force_list=force_list,
        )

        _LOGGER.info(f"Returning data for {len(scan_schedules)} scan schedules...")
        return scan_schedules

    def list_scans(
        self,
        force_list=None,
    ):
        """List all scans in Qualys.

        :param list force_list: A list of keys to force into list format when parsing
            the returned XML into lists and dictionaries. Defaults to ``None``.
        :return list: A list of dicts, containing metadata for all Qualys scans.
        """
        # TODO: looping for all scans? limit?
        _LOGGER.info("Requesting scan data from Qualys...")
        _LOGGER.debug(f"Args: force_list={force_list}")
        scan_data = self._make_list_request(
            "/api/2.0/fo/scan/",
            "SCAN",
            force_list=force_list,
        )
        _LOGGER.info(f"Returning data for {len(scan_data)} scans...")
        return scan_data

    def _get_scanref_result(
        self,
        scan_ref,
        output_format=DEFAULT_SCAN_RESULT_OUTPUT_FORMAT,
        mode=DEFAULT_SCAN_RESULT_MODE,
    ):
        """Provided a scan reference ID, fetches the scan result from Qualys.

        :param str scan_ref: The scan reference ID, e.g. ``"scan/123456789.12345"``
        :param str output_format: The output format of the scan results. Must be
            one of: "csv", "json", "csv_extended", "json_extended".
            Defaults to ``bibt.qualys.DEFAULT_SCAN_RESULT_OUTPUT_FORMAT``.
        :param str mode: Must be one of "brief" or "extended". Specifies the level
            of detail per result for Qualys to return. Defaults to
            ``bibt.qualys.DEFAULT_SCAN_RESULT_MODE``.
        :return list OR str: The scan result in the requested output format.
        """
        # TODO: fetch req func
        request_url = self.url + "/api/2.0/fo/scan/"
        params = {
            "action": "fetch",
            "scan_ref": scan_ref,
            "output_format": output_format,
            "mode": mode,
        }
        resp = self._handle_request(self.session.get(request_url, params=params))
        logging.debug(resp.text[: min(len(resp.text), 300)] + "...")

        if output_format in ["json", "json_extended"]:
            return resp.json()
        else:
            return resp.text

    def get_scan_result(
        self,
        scan_title,
        output_format=DEFAULT_SCAN_RESULT_OUTPUT_FORMAT,
        mode=DEFAULT_SCAN_RESULT_MODE,
        accept_scan_states=None,
        refactor_json_data=True,
    ):
        """Given a scan title, will fetch the most recent scan result.

        :param str scan_title: The title of the scan, e.g. "VLAN 100 Scan".
        :param str output_format: The output format of the scan results. Must be
            one of: "csv", "json", "csv_extended", "json_extended".
            Defaults to ``bibt.qualys.DEFAULT_SCAN_RESULT_OUTPUT_FORMAT``.
        :param str mode: Must be one of "brief" or "extended". Specifies the level
            of detail per result for Qualys to return. Defaults to
            ``bibt.qualys.DEFAULT_SCAN_RESULT_MODE``.
        :param list accept_scan_states: A list of scan statuses to accept,
            in addition to "Finished". Other potential scan states are:
            "Queued", "Running", "Loading", "Canceling", "Canceled", "Pausing",
            "Paused", "Resuming", and "Error". Note that it may not be possible to
            get results for any or all of these other scan states. Defaults to ``None``.
        :param bool refactor_json_data: Whether or not to refactor "json_extended" scan
            result data into a more organized format. By default, Qualys returns a list
            of dictionaries, where: the first two dictionaries cover request metadata
            and scan result metadata respectively; the last dictionary includes special
            notes about the scan run; and each of the dictionaries in the middle contain
            result data per host. If this option is set to True, the data will be
            reformated to a dictionary with the keys: ``"request_metadata": {}``,
            ``"scan_metadata": {}``, ``"scan_notes": {}``, and ``"results": [{}, {}]``.
            Defaults to ``True``.
        :raises Exception: If no scan result is found for the given title.
        :return list OR dict OR str: THe scan result data.
        """
        _LOGGER.info(f"Getting scan result for scan [{scan_title}]...")
        _LOGGER.debug(
            f"Args: scan_title=[{scan_title}] "
            f"output_format=[{output_format}] mode=[{mode}]"
        )
        all_scans = self.list_scans()
        scan_ref = None
        logging.debug(
            f"Iterating through {len(all_scans)} scans to find right scan_ref..."
        )
        if isinstance(accept_scan_states, list):
            accept_scan_states.extend(["Finished"])
        else:
            accept_scan_states = ["Finished"]
        for scan in all_scans:
            if scan["TITLE"] == scan_title:
                if scan["STATUS"]["STATE"] in accept_scan_states:
                    logging.debug(
                        "Matching scan found! ref: "
                        f'[{scan["REF"]}] state: [{scan["STATUS"]["STATE"]}] '
                        f'launched: [{scan["LAUNCH_DATETIME"]}]'
                    )
                    scan_ref = scan["REF"]
                    break
                else:
                    logging.debug(
                        "Matching scan found, but has state: "
                        f'[{scan["STATUS"]["STATE"]}] ref: [{scan["REF"]}]  '
                        f'launched: [{scan["LAUNCH_DATETIME"]}]'
                    )

        if not scan_ref:
            raise Exception(f"No scan found for title: [{scan_title}]")

        scan_data = self._get_scanref_result(
            scan_ref, output_format=output_format, mode=mode
        )
        if (
            output_format == "json_extended"
            and refactor_json_data
            and len(scan_data) >= 3
        ):
            if (
                "target_distribution_across_scanner_appliances" in scan_data[-1]
                or "hosts_not_scanned_host_not_alive_ip" in scan_data[-1]
                or "no_vulnerabilities_match_your_filters_for_these_hosts"
                in scan_data[-1]
            ):
                return {
                    "request_metadata": scan_data[0],
                    "scan_metadata": scan_data[1],
                    "scan_notes": scan_data[-1],
                    "results": scan_data[2:-1],
                }
            else:
                return {
                    "request_metadata": scan_data[0],
                    "scan_metadata": scan_data[1],
                    "results": scan_data[2:],
                }
        return scan_data

    def delete_scan_result(self, scan_ref):
        """Deletes a scan result from Qualys by its reference ID.

        :param str scan_ref: The scan reference ID, e.g. ``"scan/123456789.12345"``
        """
        _LOGGER.info(f"Sending delete request for scan: [{scan_ref}]")
        self._make_delete_request("/api/2.0/fo/scan/", scan_ref)
        _LOGGER.info(f"Scan [{scan_ref}] deleted.")

    # def get_report(self, report_title):
    # def get_kb(self)

    def search_hostassets(self, data, clean_data=True):
        # TODO: data cleaning?
        if not self.session:
            raise Exception(
                "Cannot make requests via a closed HTTP session! "
                "Please create a new Client object to initialize a new session."
            )

        _LOGGER.info("Requesting host asset data from Qualys...")
        request_url = self.url + "/qps/rest/2.0/search/am/hostasset"
        _LOGGER.debug(f"Request url: {request_url}")
        resp = self._handle_request(
            self.session.post(
                request_url, headers={"Accept": "application/json"}, data=data
            )
        )
        _LOGGER.debug(resp.text)
        resp_json = resp.json()["ServiceResponse"]["data"]
        host_assets = []
        for host_asset in resp_json:
            if clean_data:
                _LOGGER.info("Cleaning data...")
                pass
                # host_asset_data = json.dumps(host_asset["HostAsset"])
                # try:
                #     bq_values_of_death = [": {}", ": []"]
                #     for val in bq_values_of_death:
                #         if val in host_asset_data:
                #             host_asset_data = (
                #                 str(host_asset_data)
                #                 .replace(": {}", ": null")
                #                 .replace(": []", ": null")
                #             )
                # except Exception as e:
                #     logging.info(
                #         f"Replacing the BQ values of death failed with error: {e}"
                #     )
            host_assets.append(host_asset["HostAsset"])
        _LOGGER.info(f"Returning data for {len(host_assets)} host assets...")
        return host_assets
