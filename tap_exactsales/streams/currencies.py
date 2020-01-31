from tap_exactsales.stream import ExactsalesStream


class CurrenciesStream(ExactsalesStream):
    endpoint = 'currencies'
    schema = 'currency'
    key_properties = ['id', ]
