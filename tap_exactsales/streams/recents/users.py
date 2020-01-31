from tap_exactsales.streams.recents import RecentsStream


class RecentUsersStream(RecentsStream):
    items = 'user'
    schema = 'users'
    key_properties = ['id', ]
    # temporary disabled due current Exactsales API limitations
    # state_field = 'modified'

    def process_row(self, row):
        return row['data'][0]
