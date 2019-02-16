===============
Swagger Setup
===============

The purpose of this document is to help developers locally view the API documentation.

Steps:
=======================
    1. Download swagger-ui from https://github.com/swagger-api/swagger-ui
    2. Unzip the folder and copy the 'swagger' folder from your local repo into `.\swagger-ui-master\swagger-ui-master\dist`
    3. Open index.html file (with any text editor of your choice) located in `.\swagger-ui-master\swagger-ui-master\dist`
    4. On line 42, replace the default URL with `swagger/swagger.yaml`
    5. Open index.html (with any browser of your choice) to view swagger