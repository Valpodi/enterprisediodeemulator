# Copyright PA Knowledge Ltd 2021
# For licence terms see LICENCE.md file

import connexion

app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('openapispec.yaml')
app.run(port=8081)

