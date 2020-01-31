from tap_exactsales.stream import ExactsalesStream


class ActivityTypesStream(ExactsalesStream):
    endpoint = 'activityTypes'
    schema = 'activity_types'
    key_properties = ['id', ]
    state_field = 'update_time'
