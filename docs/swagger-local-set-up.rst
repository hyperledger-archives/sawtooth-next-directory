===============
Swagger Setup
===============

The purpose of this document is to help developers locally view the API documentation.

Steps:
=======================
    1. Clone swagger-ui from https://github.com/swagger-api/swagger-ui
    2. Copy the 'swagger' folder from your local sawtooth-next-directpry repo into `swagger-ui-master/dist`
    3. Inside `swagger-ui-master/dist` open index.html file (with any text editor of your choice)
    4. On line 42, replace the default URL with `swagger/swagger/swagger.yaml`
    5. Open index.html (with any browser of your choice) to view swagger
    6. If you are using Chrome. Open Chrome using command line `open -a Google\ Chrome --args --disable-web-security --user-data-dir=""`