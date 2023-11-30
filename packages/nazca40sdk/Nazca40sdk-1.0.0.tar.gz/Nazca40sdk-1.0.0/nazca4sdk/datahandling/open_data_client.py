"""OpenData Client module"""
import datetime
import io
import json
from typing import List, Optional

import requests
from requests.exceptions import ConnectionError

from nazca4sdk.datahandling.cache.key_value import KeyValue
from nazca4sdk.datahandling.data_mod import Data
from nazca4sdk.datahandling.hotstorage.helper import get_variable_table_name
from nazca4sdk.datahandling.hotstorage.user_variable_value import UserVariableValue, UserVariablesValues
from nazca4sdk.datahandling.hotstorage.user_variables_info_value import UserVariablesInfoValues
from nazca4sdk.datahandling.hotstorage.user_variables_stats_info import UserVariablesStatsInfo
from nazca4sdk.datahandling.hotstorage.variables_stats_info import VariableStatsInfo
from nazca4sdk.datahandling.hotstorage.helper import get_variable_table_name
from nazca4sdk.datahandling.npoe.boot_profiles import BootProfiles, BootProfile
from nazca4sdk.datahandling.npoe.connection import Connections
from dependency_injector.wiring import inject

JSON_HEADERS = {'Content-Type': 'application/json',
                'Accept': 'application/json'}


class DateTimeAwareEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class OpenDataClient:
    """
    Get data from OpenData

    """
    @inject
    def __init__(self, url: str,  https: str):
        """
        Initialize OpenData url to receive system configuration
        """
        if https == "True":
            self.base_url = f'https://{url}:5001'
        else:
            self.base_url = f'http://{url}:80'

    @staticmethod
    def parse_response(response):
        """
        Parsing method

        """
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("OpenData response failure")
                return None
            return Data(json_response)

        print("OpenData response error")
        return None

    def get_paged_data(self, url: str, params: list, page_size=10000):
        """
        Get request to url with params and return result array of page

        Args:
            url: url to endpoint
            params: params to get request
            page_size: size of page

        Returns:
            array of  values : Paged values
        Example:
            get_page_data(url='/api/hotstorage/ReadHistoricalVariable', params=[('start_date','2022-12-16T00:00:00')],
            page_size=100)
        """

        api_url = f'{self.base_url}{url}'
        page_number = 1
        result = []
        session = requests.Session()
        headers = JSON_HEADERS
        try:
            params.append(('pageSize', page_size))
            p = params.copy()
            p.append(('pageNumber', page_number))
            response = session.get(
                api_url,
                params=params,
                headers=headers, verify=False)
            if response.status_code == 200:
                result = response.json()
            yield result
            result_page_size = len(result)
            page_number = page_number + 1
            while result_page_size == page_size:
                pa = params.copy()
                pa.append(('pageNumber', page_number))
                result = session.get(api_url, params=pa, headers=headers, verify=False).json()
                result_page_size = len(result)
                page_number = page_number + 1
                yield result
        except AttributeError:
            print('Can not mix time descriptions, use start_date end_date'
                  ' or time amount with time unit')
            return None

    def request_params(self, module_name, grouped_variables, **time):
        """
        Creates request for OpenData

        Args:
            module_name: module_name
            grouped_variables: list of variable names
            time: **time - Time definition:
                Possible pairs: start_date end_date or time_amount time_unit
        Returns:
            request for Open Data
        """
        headers = JSON_HEADERS
        try:
            if time.get("start_date") and time.get("end_date") is not None:
                request_params = [
                    ('module', module_name),
                    ('startdate', time['start_date']),
                    ('enddate', time['end_date'])
                ]

                for variable_type in grouped_variables:
                    for variable_name in variable_type[1]:
                        request_params.append((f'groupedVariables[{variable_type[0]}]',
                                               variable_name))

                response = requests.get(
                    f'{self.base_url}/api/HotStorage/VariableOverTime',
                    params=request_params,
                    headers=headers, verify=False)
                return response

        except AttributeError:
            print('Can not mix time descriptions, use start_date end_date'
                  ' or time amount with time unit')
            return None

    def save_variables(self, user_variables: [UserVariableValue]):
        if not isinstance(user_variables, list):
            raise ValueError("user variable is not a list")
        if not all(isinstance(x, UserVariableValue) for x in user_variables):
            raise ValueError("All object in user_variable list should by type UserVariable")
        headers = JSON_HEADERS
        try:
            variables = UserVariablesValues(__root__=user_variables)
            request_params = variables.json()
            response = requests.post(
                f'{self.base_url}/api/HotStorage/saveUserVariables',
                data=request_params,
                headers=headers, verify=False)
            return response

        except AttributeError:
            print('Can not mix time descriptions, use start_date end_date'
                  ' or time amount with time unit')
            return None

    def read_variables(self, user_variables_info: UserVariablesInfoValues):
        headers = JSON_HEADERS
        try:
            request_params = [
                ('startdate', user_variables_info.startDate),
                ('enddate', user_variables_info.endDate)
            ]

            for variable_type in user_variables_info.variables:
                for variable_name in user_variables_info.variables[variable_type]:
                    request_params.append((f'variables[{variable_type}]', variable_name))

            response = requests.get(
                f'{self.base_url}/api/HotStorage/userVariablesOverTime',
                params=request_params,
                headers=headers, verify=False)
            return response

        except AttributeError:
            print('Can not mix time descriptions, use start_date end_date'
                  ' or time amount with time unit')
            return None

    def download_file(self, path: str, local_path: str):
        """download file from file storage

        Args:
            path: path to file
            local_path: path to save the file

        Returns:
            binary of  file

        """
        headers = JSON_HEADERS
        try:
            request_params = [('path', path)]
            response = requests.get(
                f'{self.base_url}/api/FileRepository/file',
                params=request_params,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return False
        except AttributeError:
            print(f'error while downloading file {path} from file repository')
            return False
        if response.status_code == 200:
            f = open(local_path, "wb")
            f.write(bytes(response.content))
            f.close()
            return True
        print(f"Error downloading file {path}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return False

    def send_file(self, path: str, file: io.BytesIO):
        r"""send file to file storage

        Args:
            file: binary file to send
            path: path to file on file storage

        Returns:
            True - file saved, False - file save error

        """

        try:
            files = {'file': ("File.txt", file, "application/octet-stream")}
            request_params = [('path', path)]
            response = requests.post(
                f'{self.base_url}/api/FileRepository/file',
                params=request_params,
                files=files,
                verify=False)
        except ConnectionError as e:
            print(f'Failed to establish connection to OpenData {e}')
            return None
        except AttributeError:
            print(f'error while sending file {path} to file repository')
            return False
        if response.status_code == 200 or response.status_code == 204:
            print(f"file {path} saved.")
            return True
        print(f"Error sending file {path}, status code = {response.status_code}")
        return False

    def read_cache_keys(self, keys):
        headers = {'Accept': 'application/json'}
        try:

            request_params = {}
            for index in range(0, len(keys)):
                request_params[f"keys[{index}]"] = keys[index]

            response = requests.get(
                f'{self.base_url}/api/Cache',
                params=request_params,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return None
        except AttributeError:
            print(f'error while get values for keys - {keys}')
            return None
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("OpenData response failure")
                return None
            return json_response
        print(f"error while get values for keys - {keys}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return None

    def write_cache_keys(self, key_values: KeyValue):
        """write key value to cache
        Args:
            key_values: dict key, value
        Returns:
              CacheEntry json if value saved or None if error
        """
        headers = JSON_HEADERS
        try:

            request_params = {"key": key_values.key,
                              "value": key_values.value}
            dump = json.dumps(request_params, cls=DateTimeAwareEncoder)
            response = requests.post(
                f'{self.base_url}/api/Cache/writeKeyValue',
                data=dump,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return None
        except AttributeError:
            print(f'error while write values - {key_values}')
            return None
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("OpenData response failure")
                return None
            return json_response
        print(f"error while write cache values - {key_values}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return None

    def read_knowledge_keys(self, name=None, ts_min=None, ts_max=None, size=0):
        headers = {'Accept': 'application/json'}
        try:
            request_params = {
                "key": name,
                "ts_min": ts_min,
                "ts_max": ts_max,
                "size": size
            }
            response = requests.get(
                f'{self.base_url}/api/knowledge/knowledgeKeys',
                params=request_params,
                headers=headers,
                verify=False)
        except ConnectionError:
            print('Failed to establish connection to OpenData')
            return None
        except AttributeError:
            print(f'error while get knowledge keys')
            return None
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("Get knowledge  failure")
                return None
            return json_response
        print(f"error while get knowledge keys, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return None

    def read_knowledge_values(self, key):
        headers = {'Accept': 'application/json'}
        try:

            request_params = {
                "key": key
            }

            response = requests.get(
                f'{self.base_url}/api/knowledge',
                params=request_params,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return None
        except AttributeError:
            print(f'error while get knowledge for key - {key}')
            return None
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("Get knowledge  failure")
                return None
            return json_response
        print(f"error while get knowledge for key - {key}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return None

    def delete_knowledge_keys(self, keys):
        headers = {'Accept': 'application/json'}
        try:
            request_params = {}
            for index in range(0, len(keys)):
                request_params[f"keys[{index}]"] = keys[index]

            response = requests.delete(
                f'{self.base_url}/api/knowledge/keys',
                params=request_params,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return None
        except AttributeError:
            print(f'error while get values for keys - {keys}')
            return None
        if response.status_code == 200:
            return int(response.content)
        print(f"error while get values for keys - {keys}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return None

    def delete_knowledge_sections(self, sections, key):
        headers = {'Accept': 'application/json'}
        try:
            if type(sections) != list:
                print('The ''sections'' argument is not a list')
                return False
            request_params = {}
            for index in range(0, len(sections)):
                request_params[f"sections[{index}]"] = sections[index]
            request_params["key"] = key

            response = requests.delete(
                f'{self.base_url}/api/knowledge/sections',
                params=request_params,
                headers=headers,
                verify=False)
        except ConnectionError:
            print(' Failed to establish connection to OpenData')
            return None
        except AttributeError:
            print(f'error while get values for keys - {key}')
            return None
        if response.status_code == 200:
            return response.content
        print(f"error while get values for keys - {key}, response.status_code={response.status_code}, "
              f"response.content={response.content}")
        return None

    def read_nazca_variables(self):
        headers = {'Accept': 'application/json'}
        response = requests.get(
            f'{self.base_url}/api/NazcaVariables', headers=headers, verify=False)
        return response

    def read_nazca_variable(self, identifier: str):
        headers = {'Accept': 'application/json'}
        response = requests.get(
            f'{self.base_url}/api/NazcaVariables/{identifier}', headers=headers, verify=False)
        return response

    def read_variables_stats(self, variables_stats_info: VariableStatsInfo):
        headers = JSON_HEADERS
        try:
            request_params = [
                ('startdate', variables_stats_info.startDate),
                ('enddate', variables_stats_info.endDate),
                ('module', variables_stats_info.module)
            ]

            for variable_type in variables_stats_info.variables:
                for variable_name in variables_stats_info.variables[variable_type]:
                    request_params.append((f'variables[{variable_type}]', variable_name))

            response = requests.get(
                f'{self.base_url}/api/HotStorage/variablesStats',
                params=request_params,
                headers=headers, verify=False)
            return response

        except AttributeError:
            print('Attribute error')
            return None

    def read_user_variables_stats(self, info: UserVariablesStatsInfo):
        headers = JSON_HEADERS
        try:
            request_params = [
                ('startdate', info.startDate),
                ('enddate', info.endDate)
            ]

            for variable in info.variables:
                var_type = get_variable_table_name(variable.type)
                if var_type is None:
                    print(f"Variable type {variable.type} not recognized")
                request_params.append((f'variables[{var_type}]', variable.name))

            response = requests.get(
                f'{self.base_url}/api/HotStorage/uservariablesStats',
                params=request_params,
                headers=headers, verify=False)
            return response

        except AttributeError:
            print('Attribute error')
            return None

    def get_boot_profiles(self) -> Optional[List[BootProfile]]:
        headers = JSON_HEADERS
        try:
            response = requests.get(
                f'{self.base_url}/api/Config/npoe/bootprofiles',
                headers=headers, verify=False)
            return BootProfiles.parse_raw(response.content).boot_profiles()

        except AttributeError:
            print('Attribute error')
            return None

    def set_boot_profiles_as_recorded(self, profile_ids: List[str]):
        headers = JSON_HEADERS
        try:
            requests.post(
                f'{self.base_url}/api/Config/npoe/bootprofiles/recorded',
                headers=headers, verify=False, json={"guids": profile_ids})

        except Exception:
            print('Attribute error')
            return None

    def get_connections(self):
        headers = JSON_HEADERS
        try:
            response = requests.get(
                f'{self.base_url}/api/Config/connections',
                headers=headers, verify=False)
            return Connections.parse_raw(response.content).connections()

        except AttributeError:
            print('Attribute error')
            return None
