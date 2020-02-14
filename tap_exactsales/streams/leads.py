from tap_exactsales.stream import ExactsalesIterStream


class LeadsStream(ExactsalesIterStream):
    base_endpoint = 'listarlead'
    endpoint = 'listarlead'
    schema = 'leads'
    key_properties = ['id']
    state_field = 'DtAtualizacao'
    pagination = True

    def get_name(self):
        return self.schema

    def update_endpoint(self):
        self.endpoint = "{}?DtCadastroInicio={}&DtAtualizacao={}&page={}&max_results={}".format(self.base_endpoint, self.initial_state.strftime('%Y-%m-%d'), self.earliest_state.strftime('%Y-%m-%d'), self.start, self.limit)
