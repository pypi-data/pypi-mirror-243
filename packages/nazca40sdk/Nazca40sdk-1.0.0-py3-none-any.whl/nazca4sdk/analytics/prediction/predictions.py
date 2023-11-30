"""Module for predictions with Prophet/Nixtla"""
from pydantic import ValidationError
from nazca4sdk.analytics.__brain_connection import BrainClient
from dataclasses import dataclass


@dataclass
class Predictions:
    """
    Prediction Class

    Attributes:
        module_name: str
        variable_names: str
        time_amount: int
        time_unit: str
        forecast_time_amount: int
        forecast_time_unit: str
        prediction_tool: str


    Methods:

        forecast_prediction()
            Determine prediction values for determined input
    """
    module_name: str
    variable_names: str
    time_amount: int
    time_unit: str
    forecast_time_amount: int
    forecast_time_unit: str
    prediction_tool: str


def forecast_prediction(prediction_info: Predictions):
    """Function to determine prediction values for determined input

    Args:
        prediction_info: prediction_info
    Returns:
        dict: prediction parameters
    """

    brain = BrainClient()

    try:
        input_data = {
            "module_name": prediction_info.module_name,
            "variable_names": prediction_info.variable_names,
            "time_amount": prediction_info.time_amount,
            "time_unit": prediction_info.time_unit,
            "forecast_time_amount": prediction_info.forecast_time_amount,
            "forecast_time_unit": prediction_info.forecast_time_unit,
            "prediction_tool": prediction_info.prediction_tool
        }

        data = {**input_data}

        response = brain.get_prediction(data)
        result = brain.parse_response(response)

        return result

    except ValidationError as error:
        print(error.json())
        return None
