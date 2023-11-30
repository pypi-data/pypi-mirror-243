""" Module to communicate with Brain"""
import json

import requests


class BrainClient:
    """ Get data from Nazca4.0 Brain
    """

    def __init__(self):
        """Initialize Brain connection info"""
        self.__brain_url = 'http://brain:8000'

    def get_optimal_contracted_capacity(self, start_date: str, end_date: str, connection: str,
                                        simulated_ordered_power: int,
                                        ordered: bool, simulated: bool):
        """ Posting data to receive optimal contracted capacity calculations from Brain"""
        return requests.post(f'{self.__brain_url}/optimal_contracted_capcity/', json={
                                                                    "start_date": start_date,
                                                                    "end_date": end_date,
                                                                    "connection": connection,
                                                                    "simulated_ordered_power": simulated_ordered_power,
                                                                    "ordered": ordered,
                                                                    "simulated": simulated})

    def get_energy_quality(self, module: str, npoe: bool):
        """ Posting data to receive energy quality calculations from Brain"""
        if npoe:
            return requests.post(f'{self.__brain_url}/energy/npoe', json={"meter": module})
        return requests.post(f'{self.__brain_url}/energy/nazca', json={"module_name": module})

    def get_energy_quality_by_params(self, params: dict):
        """ Posting data to receive energy quality calculations from Brain"""
        return requests.post(f'{self.__brain_url}/energy_by_params/', json=params)

    def get_vibration_quality(self, group: str, module: str):
        """ Posting data to receive vibration quality calculations from Brain"""
        return requests.post(f'{self.__brain_url}/vibration/', json={"module_name": module, "group": group})

    def get_vibration_quality_by_params(self, group: str, vibration: float):
        """ Posting data to receive vibration quality calculations from Brain"""
        return requests.post(f'{self.__brain_url}/vibration_by_params/', json={"group": group, "vibration": vibration})

    def get_oee_easy(self, oee_easy_input):
        """ Posting data to receive OEE value based on:
            Availability, Performance, Quality parameters from Brain """
        return requests.post(f'{self.__brain_url}/oee_easy/', json=oee_easy_input)

    def get_oee_full(self, oee_full_input):
        """ Posting data to receive oee value based on A, B, C, D, E, F parameters from Brain"""
        return requests.post(f'{self.__brain_url}/oee_full/', json=oee_full_input)

    def get_cp_indicator(self, cp_input):
        """
        Posting data to receive Cp indicator
        """

        return requests.post(f'{self.__brain_url}/cp_indicator/', json=cp_input)

    def get_pp_indicator(self, pp_input):
        """
        Posting data to receive Pp indicator
        """

        return requests.post(f'{self.__brain_url}/pp_indicator/', json=pp_input)

    def get_cpk_indicator(self, cpk_input):
        """
        Posting data to receive Cpk indicator
        """
        return requests.post(f'{self.__brain_url}/cpk_indicator/', json=cpk_input)

    def get_ppk_indicator(self, ppk_input):
        """
        Posting data to receive Ppk indicator
        """
        return requests.post(f'{self.__brain_url}/ppk_indicator/', json=ppk_input)

    def get_prediction(self, prediction_input):
        """
        Posting data to receive prediction value based on: module_name, variable_name, time_amount, time_unit,
        forecast_time_amount, forecast_unit parameters from Brain
        """
        return requests.post(f'{self.__brain_url}/prediction/', json=prediction_input)

    @staticmethod
    def parse_response(response):
        """ Parsing method"""
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("Brain response failure")
                return None
            return json_response
        print("Brain response error")
        try:
            print(json.dumps(response.json(), indent=4))
        except:
            print("Code: ", response.status_code)
        return None
