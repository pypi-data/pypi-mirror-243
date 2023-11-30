"""Analytics module"""
from nazca4sdk.analytics.performance_indicators.indicators import Indicators
from nazca4sdk.analytics.energy.energy import Energy
from nazca4sdk.analytics.vibration.vibration_quality import VibrationQuality
from nazca4sdk.analytics.prediction.forecasting import Forecasting
from nazca4sdk.system.system_cache import SystemCache
from dependency_injector.wiring import inject


class Analytics:
    """
    Analytics module as a second layer of analytics functions to use with SDK
    """

    @inject
    def __init__(self, cache: SystemCache):
        #: :class:`nazca4sdk.analytics.performance_indicators.indicators.Indicators` Module for determining key performance indicators (such as OEE, Cp, Cpk, etc.)
        self.kpi = Indicators()
        #: :class:`nazca4sdk.analytics.energy.energy.Energy` Module for calculations related to electricity (such as energy quality)
        self.energy = Energy()
        #: :class:`nazca4sdk.analytics.vibration.vibration_quality.VibrationQuality` Module for calculations related to vibrations (such as vibration quality)
        self.vibration = VibrationQuality()
        #: :class:`nazca4sdk.analytics.prediction.forecasting.Forecasting` Module for time series forecasting
        self.forecasting = Forecasting(cache)
