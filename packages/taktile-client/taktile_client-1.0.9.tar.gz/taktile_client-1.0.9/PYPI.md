# Taktile Client

[![pypi status](https://img.shields.io/pypi/v/taktile-client.svg)](https://pypi.python.org/pypi/taktile-client)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

Taktile enables data science teams to industrialize, scale, and maintain machine learning models. Our ML development platform makes it easy to create your own end-to-end ML applications:

- Turn models into auto-scaling APIs in a few lines of code
- Easily add model tests
- Create and share model explanations through the Taktile UI

`taktile-client` is a stand-alone python client which can be used to make requests to Taktile deployments via REST or [Arrow Flight](https://arrow.apache.org/docs/format/Flight.html). If you require the full Taktile dev tooling, consider installing [taktile-cli](https://pypi.org/project/taktile-cli/) instead. Find more information in our [docs](https://docs.taktile.com).

To install the REST client only, run `pip install taktile-client`. For both REST and Arrow, run `pip install taktile-client\[arrow]`.
