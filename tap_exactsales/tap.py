import time
import pendulum
import requests
import singer
from requests.exceptions import ConnectionError, RequestException
from json import JSONDecodeError
from singer import set_currently_syncing, metadata
from singer.catalog import Catalog, CatalogEntry, Schema
from .config import BASE_URL, CONFIG_DEFAULTS
from .exceptions import InvalidResponseException
from .streams import (LeadsStream)


logger = singer.get_logger()


class ExactsalesTap(object):
    streams = [
        LeadsStream()
    ]

    def __init__(self, config, state):
        self.config = self.get_default_config()
        self.config.update(config)
        self.config['start_date'] = pendulum.parse(self.config['start_date'])
        self.state = state

    def do_discover(self):
        logger.info('Starting discover')

        catalog = Catalog([])

        for stream in self.streams:
            stream.tap = self

            schema = Schema.from_dict(stream.get_schema())
            key_properties = stream.key_properties

            metadata = []
            for prop, json_schema in schema.properties.items():
                inclusion = 'available'
                if prop in key_properties or (stream.state_field and prop == stream.state_field):
                    inclusion = 'automatic'
                metadata.append({
                    'breadcrumb': ['properties', prop],
                    'metadata': {
                        'inclusion': inclusion
                    }
                })

            catalog.streams.append(CatalogEntry(
                stream=stream.schema,
                tap_stream_id=stream.schema,
                key_properties=key_properties,
                schema=schema,
                metadata=metadata
            ))

        return catalog

    def do_sync(self, catalog):
        logger.debug('Starting sync')

        # resuming when currently_syncing within state
        resume_from_stream = False
        if self.state and 'currently_syncing' in self.state:
            resume_from_stream = self.state['currently_syncing']

        selected_streams = self.get_selected_streams(catalog)

        if 'currently_syncing' in self.state and resume_from_stream not in selected_streams:
            resume_from_stream = False
            del self.state['currently_syncing']

        for stream in self.streams:
            if stream.schema not in selected_streams:
                continue

            stream.tap = self

            if resume_from_stream:
                if stream.schema == resume_from_stream:
                    logger.info('Resuming from {}'.format(resume_from_stream))
                    resume_from_stream = False
                else:
                    logger.info('Skipping stream {} as resuming from {}'.format(stream.schema, resume_from_stream))
                    continue

            # stream state, from state/bookmark or start_date
            stream.set_initial_state(self.state, self.config['start_date'])

            # currently syncing
            if stream.state_field:
                set_currently_syncing(self.state, stream.schema)
                self.state = singer.write_bookmark(self.state, stream.schema, stream.state_field, str(stream.initial_state))
                singer.write_state(self.state)

            # schema
            stream.write_schema()

            catalog_stream = catalog.get_stream(stream.schema)
            stream_metadata = metadata.to_map(catalog_stream.metadata)

            self.do_paginate(stream, stream_metadata)
                
            # set the attribution window so that the bookmark will reflect the new initial_state for the next sync
            stream.earliest_state = stream.stream_start.subtract(hours=3)
            
            # update state / bookmarking only when supported by stream
            if stream.state_field:
                self.state = singer.write_bookmark(self.state, stream.schema, stream.state_field,
                                                   str(stream.earliest_state))
            singer.write_state(self.state)

        # clear currently_syncing
        try:
            del self.state['currently_syncing']
        except KeyError as e:
            pass
        singer.write_state(self.state)

    def get_selected_streams(self, catalog):
        selected_streams = set()
        for stream in catalog.streams:
            # mdata = metadata.to_map(stream.metadata)
            # root_metadata = mdata.get(())
            selected_streams.add(stream.tap_stream_id)
        return list(selected_streams)

    def do_paginate(self, stream, stream_metadata):
        
        # note when the stream starts syncing
        stream.stream_start = pendulum.now('UTC') # explicitly set timezone to UTC

        # create checkpoint at inital_state to only find stage changes more recent than initial_state (bookmark)
        checkpoint = stream.initial_state

        must_get = True
        while must_get:
            stream.update_endpoint()
            with singer.metrics.http_request_timer(stream.schema) as timer:
                try:
                    response = self.execute_stream_request(stream)
                except (ConnectionError, RequestException) as e:
                    raise e
                timer.tags[singer.metrics.Tag.http_status_code] = response.status_code

            self.validate_response(stream, response)
            self.rate_throttling(response)
            
            stream.start = stream.start + 1

            # records with metrics
            with singer.metrics.record_counter(stream.schema) as counter:
                with singer.Transformer(singer.NO_INTEGER_DATETIME_PARSING) as optimus_prime:
                    for row in self.iterate_response(response):
                        row = stream.process_row(row)

                        if not row: # in case of a non-empty response with an empty element
                            continue
                        row = optimus_prime.transform(row, stream.get_schema(), stream_metadata)
                        if stream.write_record(row):
                            counter.increment()
                        stream.update_state(row)
            
            must_get = len(stream.payload) == stream.limit

    def get_default_config(self):
        return CONFIG_DEFAULTS

    def iterate_response(self, response):
        payload = response.json()
        return [] if payload is None else payload

    def execute_stream_request(self, stream):
        params = {
        }
        params = stream.update_request_params(params)
        return self.execute_request(stream.endpoint, params=params)

    def execute_request(self, endpoint, params=None):
        headers = {
            'token_exact': self.config['api_token']
        }
        _params = {
        }
        if params:
            _params.update(params)

        url = "{}/{}".format(BASE_URL, endpoint)
        logger.info('Firing request at {} with params: {}'.format(url, _params))

        return requests.get(url, headers=headers, params=_params)

    def validate_response(self, stream, response):
        if isinstance(response, requests.Response) and response.status_code == 200:
            try:
                stream.payload = response.json()
                return True
            except (AttributeError, JSONDecodeError) as e:
                pass
                
        raise InvalidResponseException("Response with status code {} from Exactsales API is not valid, "
                                       "wonder why ..".format(response.status_code))

    def rate_throttling(self, response):
        if all(x in response.headers for x in ['X-RateLimit-Remaining', 'X-RateLimit-Reset']):
            if int(response.headers['X-RateLimit-Remaining']) < 1:
                seconds_to_sleep = int(response.headers['X-RateLimit-Reset'])
                logger.debug('Hit API rate limits, no remaining requests per 10 seconds, will sleep '
                             'for {} seconds now.'.format(seconds_to_sleep))
                time.sleep(seconds_to_sleep)
        else:
            logger.debug('Required headers for rate throttling are not present in response header, '
                         'unable to throttle ..')

