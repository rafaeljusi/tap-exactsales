from tap_exactsales.stream import ExactsalesIterStream


class LeadsStream(ExactsalesIterStream):
    base_endpoint = 'listarlead?DtCadastroInicio=2010-01-01'
    endpoint = 'listarlead?DtCadastroInicio=2010-01-01'
    schema = 'leads'
    key_properties = ['id']
    state_field = 'DtAtualizacao'
    pagination = False

    def get_name(self):
        return self.schema