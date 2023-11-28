import json
import logging

import requests
import xmltodict

from .params import ASSET_GROUP_ATTRIBUTES_LIST
from .params import DEFAULT_SCAN_RESULT_MODE
from .params import DEFAULT_SCAN_RESULT_OUTPUT_FORMAT
from .params import DEFAULT_TRUNCATION

QUALYS_REPORT_ENDPOINT = "/api/2.0/fo/report/"
QUALYS_SCAN_ENDPOINT = "/api/2.0/fo/scan/"
QUALYS_SCAN_SCHEDULE_ENDPOINT = "/api/2.0/fo/schedule/scan/"
QUALYS_ASSET_GROUP_ENDPOINT = "/api/2.0/fo/asset/group/"
QUALYS_ASSET_HOST_ENDPOINT = "/api/2.0/fo/asset/host/"
QUALYS_CLOUD_AGENT_SEARCH_HOST_ASSET_ENDPOINT = "/qps/rest/2.0/search/am/hostasset"

_LOGGER = logging.getLogger(__name__)

# TODO: Documentation
# TODO: kwargs?


class Client:
    """Creates a ``bibt.qualys.Client`` object, which may be used to
    make Qualys API calls using the same set of credentials.

    :param str user: The Qualys username with which to authenticate.
    :param str password: The password for the provided account username.
    :param str url: The root domain for Qualys, e.g.
        ``"https://qualysapi.qg1.apps.qualys.com"``.
    """

    def __init__(self, user, password, url):
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

    #
    # Private Helper Functions
    #

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
                resp.content,
                attr_prefix="",
                cdata_key="text",
                comment_key="comment",
                force_list=force_list,
            )

            # handle special case of final key being different
            final_key = key
            if key == "SCHEDULE_SCAN":
                final_key = "SCAN"

            if f"{key}_LIST" not in resp_json[f"{key}_LIST_OUTPUT"]["RESPONSE"]:
                if len(full_resp) < 1:
                    _LOGGER.error(
                        f"Key {key}_LIST not found in data from Qualys; ensure "
                        "you have the correct permissions to fetch this data."
                    )
                    return []
                else:
                    break
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

    def _make_fetch_request(self, endpoint, params={}):
        if not self.session:
            raise Exception(
                "Cannot make requests via a closed HTTP session! "
                "Please create a new Client object to initialize a new session."
            )
        request_url = self.url + endpoint
        params["action"] = "fetch"
        resp = self._handle_request(self.session.get(request_url, params=params))
        # logging.debug(str(resp.content[: min(len(resp.content), 300)] + b"..."))

        if params.get("output_format") in ["json", "json_extended"]:
            return resp.json()
        else:
            return resp.text

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

    def _list_scans_reports(self, endpoint, key, state, force_list):
        params = {}
        if state:
            params["state"] = state
        return self._make_list_request(
            endpoint,
            key,
            params=params,
            force_list=force_list,
        )

    def _match_results(self, all_results, title, result_type):
        ref = None
        ref_key = "REF" if result_type == "SCAN" else "ID"
        logging.debug(
            f"Iterating through {len(all_results)} results to find right "
            f"ref/id for result titled [{title}]..."
        )
        for result in all_results:
            if result["TITLE"] == title:
                logging.info(
                    "Matching result found! ref: "
                    f'[{result[ref_key]}] state: [{result["STATUS"]["STATE"]}] '
                    f'launched: [{result["LAUNCH_DATETIME"]}]'
                )
                return result

        if not ref:
            raise Exception(
                f"No result found for title: [{title}] "
                f"in {len(all_results)} results."
            )

    #
    #  Asset: Groups Endpoint
    #  /api/2.0/fo/asset/groups
    #

    def list_asset_groups(
        self,
        truncation_limit=DEFAULT_TRUNCATION,
        show_attributes=ASSET_GROUP_ATTRIBUTES_LIST,
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
            QUALYS_ASSET_GROUP_ENDPOINT,
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

    #
    #  Asset: Host Endpoint
    #  /api/2.0/fo/asset/host
    #

    def list_hosts(
        self,
        truncation_limit=DEFAULT_TRUNCATION,
        show_attributes=ASSET_GROUP_ATTRIBUTES_LIST,
        force_list=None,
    ):
        _LOGGER.info("Requesting asset group data from Qualys...")
        _LOGGER.debug(
            f"Args: force_list={force_list} "
            f"truncation_limit=[{truncation_limit}] show_attributes=[{show_attributes}]"
        )
        resp = self._make_list_request(
            QUALYS_ASSET_HOST_ENDPOINT,
            "HOST",
            params={
                "truncation_limit": truncation_limit,
                "show_attributes": show_attributes,
            },
            force_list=force_list,
        )

        _LOGGER.info(f"Returning data for {len(resp)} hosts...")
        return resp

    #
    #  Scan Schedules Endpoint
    #  /api/2.0/fo/schedule/scan/
    #

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
            QUALYS_SCAN_SCHEDULE_ENDPOINT,
            "SCHEDULE_SCAN",
            force_list=force_list,
        )

        _LOGGER.info(f"Returning data for {len(scan_schedules)} scan schedules...")
        return scan_schedules

    #
    #  Scan Endpoint
    #  /api/2.0/fo/scan/
    #

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
            Defaults to ``bibt.qualys.params.DEFAULT_SCAN_RESULT_OUTPUT_FORMAT``.
        :param str mode: Must be one of "brief" or "extended". Specifies the level
            of detail per result for Qualys to return. Defaults to
            ``bibt.qualys.params.DEFAULT_SCAN_RESULT_MODE``.
        :return list OR str: The scan result in the requested output format.
        """
        _LOGGER.info(
            f"Getting results for: [{scan_ref}] in format "
            f"[{output_format}] in mode [{mode}]"
        )
        return self._make_fetch_request(
            QUALYS_SCAN_ENDPOINT,
            params={"output_format": output_format, "mode": mode, "scan_ref": scan_ref},
        )

    def list_scans(
        self,
        state="Finished",
        force_list=None,
    ):
        """List all scans in Qualys.

        :param str state: The state of scans to return. Set to ``None`` to
            return all scans. Defaults to ``"Finished"``.
        :param list force_list: A list of keys to force into list format when parsing
            the returned XML into lists and dictionaries. Defaults to ``None``.
        :return list: A list of dicts, containing metadata for all Qualys scans.
        """
        _LOGGER.info("Requesting scan data from Qualys...")
        _LOGGER.debug(f"Args: state={state} force_list={force_list}")
        scan_data = self._list_scans_reports(
            QUALYS_SCAN_ENDPOINT, "SCAN", state, force_list
        )
        _LOGGER.info(f"Returning data for {len(scan_data)} scans...")
        return scan_data

    def get_scan_result(
        self,
        scan_title,
        output_format=DEFAULT_SCAN_RESULT_OUTPUT_FORMAT,
        mode=DEFAULT_SCAN_RESULT_MODE,
        refactor_json_data=True,
    ):
        """Given a scan title, will fetch the most recent scan result.

        :param str scan_title: The title of the scan, e.g. "VLAN 100 Scan".
        :param str output_format: The output format of the scan results. Must be
            one of: "csv", "json", "csv_extended", "json_extended".
            Defaults to ``bibt.qualys.params.DEFAULT_SCAN_RESULT_OUTPUT_FORMAT``.
        :param str mode: Must be one of "brief" or "extended". Specifies the level
            of detail per result for Qualys to return. Defaults to
            ``bibt.qualys.params.DEFAULT_SCAN_RESULT_MODE``.
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

        all_scans = self.list_scans(state="Finished")

        scan = self._match_results(all_scans, scan_title, "SCAN")

        scan_data = self._get_scanref_result(
            scan["REF"], output_format=output_format, mode=mode
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
        self._make_delete_request(QUALYS_SCAN_ENDPOINT, scan_ref)
        _LOGGER.info(f"Scan [{scan_ref}] deleted.")

    #
    # Reports Endpoint
    # /api/2.0/fo/report/
    #

    def _get_reportid_result(self, report_id):
        """Provided a report ID, fetches the report result from Qualys.
            Report MUST have a state of "Finished".

        :param str report_id: The report ID, e.g. ``"123456"``.
        :return list OR str: The report result.
        """
        _LOGGER.info(f"Getting results for report: [{report_id}]")
        report_data = self._make_fetch_request(
            QUALYS_REPORT_ENDPOINT,
            params={"id": report_id},
        )
        return report_data

    def list_reports(
        self,
        state="Finished",
        force_list=None,
    ):
        """List all reports in Qualys.

        :param str state: The state of reports to return. Set to ``None`` to
            return all reports. Defaults to ``"Finished"``.
        :param list force_list: A list of keys to force into list format when parsing
            the returned XML into lists and dictionaries. Defaults to ``None``.
        :return list: A list of dicts, containing metadata for all Qualys reports.
        """
        _LOGGER.info("Requesting report data from Qualys...")
        _LOGGER.debug(f"Args: state={state} force_list={force_list}")
        report_data = self._list_scans_reports(
            QUALYS_REPORT_ENDPOINT, "REPORT", state, force_list
        )
        _LOGGER.info(f"Returning data for {len(report_data)} reports...")
        return report_data

    def get_report_result(self, report_title):
        """Given a report title, fetches the most recent report result.

        :param str report_title: The report title for which to search.
        :return (str, str): A tuple of ``(output_format, data)`` where
            ``output_format`` is the configured report output format,
            e.g. "XML", "HTML", "CSV", etc.
        """
        _LOGGER.info(f"Searching for result for report: [{report_title}]")
        all_reports = self.list_reports(state="Finished")
        report = self._match_results(all_reports, report_title, "REPORT")
        _LOGGER.debug(
            f"Fetching report result: id=[{report['ID']}] type="
            f"[{report['OUTPUT_FORMAT']}] size=[{report['SIZE']}]"
        )
        report_data = self._get_reportid_result(report["ID"])
        _LOGGER.info(
            f"Returning data for report [{report_title}] "
            f"[{report['ID']}] in format [{report['OUTPUT_FORMAT']}]"
        )
        return report["OUTPUT_FORMAT"], report_data

    def delete_report_result(self, report_id):
        """Deletes a report result from Qualys by its ID.

        :param str report_id: The report reference ID, e.g. ``"report/123456789.12345"``
        """
        _LOGGER.info(f"Sending delete request for report: [{report_id}]")
        self._make_delete_request(QUALYS_REPORT_ENDPOINT, report_id)
        _LOGGER.info(f"Report [{report_id}] deleted.")

    #
    # Cloud Agent: Host Asset Endpoint
    # /qps/rest/2.0/search/am/hostasset
    #

    def search_hostassets(self, data, clean_data=True):
        # TODO: data cleaning?
        if not self.session:
            raise Exception(
                "Cannot make requests via a closed HTTP session! "
                "Please create a new Client object to initialize a new session."
            )

        _LOGGER.info("Requesting host asset data from Qualys...")
        request_url = self.url + QUALYS_CLOUD_AGENT_SEARCH_HOST_ASSET_ENDPOINT
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
