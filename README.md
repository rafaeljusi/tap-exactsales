# tap-exactsales

This is a [Singer](https://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:
- Pulls raw data from Exactsales's [REST API](https://exactdev.docs.apiary.io/)
- Extracts the following resources from Exactsales
  - [Leads](https://exactdev.docs.apiary.io/#reference/0/lista-de-leads/listar)
- Outputs the schema for each resource
- Incrementally pulls data based on the input state


---

Copyright &copy; 2019 Jusi
