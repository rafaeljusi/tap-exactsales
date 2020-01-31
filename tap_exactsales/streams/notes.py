from tap_exactsales.stream import ExactsalesStream


class NotesStream(ExactsalesStream):
    endpoint = 'notes'
    schema = 'notes'
    key_properties = ['id', ]
    state_field = 'update_time'
