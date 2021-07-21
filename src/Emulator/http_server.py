import connexion

app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('openapispec.yaml')
app.run(port=8081)

