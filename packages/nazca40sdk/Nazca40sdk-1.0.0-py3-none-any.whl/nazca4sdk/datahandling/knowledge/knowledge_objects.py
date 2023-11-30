"""Set of classes to prepare objects for knowledge"""
import json


class FormatText():
    """Class to prepare object of Format KnowledgeDataType"""

    def __init__(self, value, **kwargs):
        """ Initializing the FormatText object

        Args:
            value: value to write to knowledge,
            **kwargs: oprional keyword arguments for Format KnowledgeDataType:
                pipe: Angular pipe name,
                args: Angular pipe parameters,
                prefix: prefix,
                suffix: suffix
                color: name of color

        Returns:
            Object to use for Format KnowledgeDataType

        Example:
            FormatText('1995-12-17T03:24:00', pipe='DatePipe', args='fullDate', prefix='Dzisiaj jest', suffix='dzien', color='red')
        """

        self.kwargs = kwargs
        self.kwargs['value'] = value

    def __str__(self):
        """ Change to proper string """

        return str(json.dumps(self.kwargs))


class FormatChart():
    """Class to prepare object of chart KnowledgeDataType"""

    def __init__(self, chart_type, module, variable, start_time, stop_time):
        """ Initializing the FormatText object

        Args:
            chart_type: type of chart to create,
            module: name of module,
            variable: name of variable to plot,
            start_time: start time of chart range,
            stop_time: stop time of chart range,
            source: name of table in ClickHouse,

        Returns:
            Object to use for Chart KnowledgeDataType

        Example:
            FormatChart('timeseries', 'Socomec', 'P', '2021-12-17T03:00:00Z', '2021-12-17T05:00:00Z')
        """
        self.chartType = chart_type
        self.properties = {
            "module": module,
            "variable": variable,
            "startTime": start_time,
            "endTime": stop_time}

    def __str__(self):
        """ Change to proper string """

        return str(json.dumps(self.__dict__))
