# tap-exactsales

This is a [Singer](https://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:
- Pulls raw data from Exactsales's [REST API](https://developers.exactsales.com/docs/api/v1/)
- Extracts the following resources from Exactsales
  - [Currencies](https://developers.exactsales.com/docs/api/v1/#!/Currencies)
  - [ActivityTypes](https://developers.exactsales.com/docs/api/v1/#!/ActivityTypes)
  - [Filters](https://developers.exactsales.com/docs/api/v1/#!/Filters)
  - [Stages](https://developers.exactsales.com/docs/api/v1/#!/Stages)
  - [Pipelines](https://developers.exactsales.com/docs/api/v1/#!/Pipelines)
  - [Goals](https://developers.exactsales.com/docs/api/v1/#!/Goals)
  - [Recent Notes](https://developers.exactsales.com/docs/api/v1/#!/Recents)
  - [Recent Users](https://developers.exactsales.com/docs/api/v1/#!/Recents)
  - [Recent Activities](https://developers.exactsales.com/docs/api/v1/#!/Recents)
  - [Recent Deals](https://developers.exactsales.com/docs/api/v1/#!/Recents)
  - [Recent Files](https://developers.exactsales.com/docs/api/v1/#!/Recents)
  - [Recent Organizations](https://developers.exactsales.com/docs/api/v1/#!/Recents)
  - [Recent Persons](https://developers.exactsales.com/docs/api/v1/#!/Recents)
  - [Recent Products](https://developers.exactsales.com/docs/api/v1/#!/Recents)
  - [Recent DeleteLogs](https://developers.exactsales.com/docs/api/v1/#!/Recents)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state


---

Copyright &copy; 2017 Stitch
