import singer
from tap_exactsales.stream import ExactsalesIterStream

class DealStageChangeStream(ExactsalesIterStream):
    base_endpoint = 'deals'
    id_endpoint = 'deals/{}/flow'
    schema = 'dealflow'
    state_field = 'log_time'
    key_properties = ['id', ]

    def get_name(self):
        return self.schema

    def process_row(self, row):
        # grab only rows that are dealChange objects with changes in add_time or stage_id
        if row['object'] == 'dealChange':
            if row['data']['field_key'] == 'add_time' or row['data']['field_key'] == 'stage_id':
                return row['data']

    def update_endpoint(self, deal_id):
        self.endpoint = self.id_endpoint.format(deal_id)