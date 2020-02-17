# tap-exactsales

This is a [Singer](https://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:
- Pulls raw data from Exactsales's [REST API](https://exactdev.docs.apiary.io/)
- Extracts the following resources from Exactsales
  - [Leads](https://exactdev.docs.apiary.io/#reference/0/lista-de-leads/listar)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

## setup

1. Install the tap
`pip install -e .`

2. Install the target
`pip install target-stitch`

3. Create and edit the tap config file (tap_config.json)
```
{
    "api_token": "YOUR_API_TOKEN",
    "start_date": "2017-01-01T00:00:00Z"
}
```

4. Create and edit the target config file (target_config.json)
```
{
    "client_id" : YOUR_CLIENT_ID,
    "token" : "YOUR_TOKEN",
    "small_batch_url": "https://api.stitchdata.com/v2/import/batch",
    "big_batch_url": "https://api.stitchdata.com/v2/import/batch",
    "batch_size_preferences": {}
}
```

5. Generate the catalog.json file
```
tap-exactsales --config tap_config.json --discover > catalog.json
```


## Run
`tap-exactsales --config tap_config.json --catalog catalog.json | target-stitch --config target_config.json >> state.json`



---

Copyright &copy; 2019 Jusi