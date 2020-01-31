from tap_exactsales.stream import ExactsalesStream


class FiltersStream(ExactsalesStream):
    endpoint = 'filters'
    schema = 'filters'
    key_properties = ['id', ]
    state_field = 'update_time'
