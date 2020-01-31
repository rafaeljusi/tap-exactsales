from tap_exactsales.stream import ExactsalesStream


class StagesStream(ExactsalesStream):
    endpoint = 'stages'
    schema = 'stages'
    key_properties = ['id', ]
    state_field = 'update_time'
