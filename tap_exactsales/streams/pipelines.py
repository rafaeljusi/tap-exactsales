from tap_exactsales.stream import ExactsalesStream


class PipelinesStream(ExactsalesStream):
    endpoint = 'pipelines'
    schema = 'pipelines'
    key_properties = ['id', ]
    state_field = 'update_time'
