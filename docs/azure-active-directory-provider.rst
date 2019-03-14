===============================
Azure Active Directory Provider
===============================

The NEXT Identity platform interacts with Azure Active Directory Provider through three syncs:

**Initial Inbound Sync**
    The initial inbound sync pulls all user and group records from Active Directory and stores it in a queue to be imported 
    to the NEXT platform. This sync will begin when the Azure daemon is first initialized. After a successful initial inbound
    sync, you would be able to see all your Azure Active Directory users and groups on the NEXT platform, including a user's
    manager and a group's members and owner.

..

**Delta Inbound Sync**
    The delta inbound sync pulls all user or group records from Azure Active Directory that have been modified since the last 
    inbound sync occurred. The records will be queued in the inbound queue and users and groups will be updated accordingly on 
    the NEXT platform. To check for users or groups that have been modified since the last sync occurred, we utilized a changelog
    event hub in Azure. A statistics query set up on the event hub will look for changes to users and groups to be ingested into the
    inbound_queue.  By default, delta inbound sync will occur by default 50 seconds.

..

**Delta Outbound Sync**
    The delta outbound sync will record all changes to users and groups as they occur on the NEXT platform by storing the changes 
    in a queue called 'outbound_queue'. From the queue, each change will be processed and Azure Active Directory will be updated 
    accordingly. The delta outbound sync will help keep your Active Directory stay up to date with the changes that are being 
    performed on NEXT.


Integrating Active Directory Provider and NEXT
==============================================

Setting up Environment Variables
--------------------------------
To connect your organization's Azure Active Directory provider to the NEXT platform, you must have an application registered with
application level credentials.  You must also have an event hub that is ingesting the audit log for your Azure instance.  
Once that has been established you must configure the following environment variables in the .env file located in the root directory.

Azure Application variables: 

* **CLIENT_ID**: The client id for your Azure application.
* **TENANT_ID**: The tenant id for your Azure application.
* **AUTH_TYPE**: The type of authorization your application is using for it's Azure credentails.  This is either 'CERT' or 'SECRET'.

If AUTH TYPE is 'SECRET':

* **CLIENT_SECRET**: The secret for your application's authorization credentials to Azure.

If AUTH TYPE is 'CERT':

* **CLIENT_ASSERTION**: The certificate for your application's authorization credentials to Azure.

Event Hub Variables:

* **AAD_EH_SAS_POLICY**: The SAS policy for your Azure event hub
* **AAD_EH_SAS_KEY**: The SAS key for your Azure event hub
* **AAD_EH_CONSUMER_GROUP**: The consumer group for your Azure event hub
* **AAD_EH_NAMESPACE**: The namespace of your Azure event hub
* **AAD_EH_NAME**: The name of your Azure event hub

Examples of these can be found in .env.example

Active Directory Data Field Mapping
----------------------------------------
When data is imported into the NEXT platform from Azure Active Directory, the data field names for users and groups will be 
mapped to new field names to allow our platform to interact with the incoming data. Active Directory data fields are currently being 
mapped according to the tables below.

User Fields

+----------------------------+----------------------+
|   Azure AD Field           |     NEXT Field       |
+============================+======================+
| id                         | next_id              |
+----------------------------+----------------------+
| deletedDateTime            | deleted_date         |
+----------------------------+----------------------+
| accountEnabled             | account_enabled      |
+----------------------------+----------------------+
| businessPhones             | business_phones      |
+----------------------------+----------------------+
| city                       | city                 |
+----------------------------+----------------------+
| createdDateTime            | created_date         |
+----------------------------+----------------------+
| companyName                | company_name         |
+----------------------------+----------------------+
| country                    | country              |
+----------------------------+----------------------+
| department                 | department           |
+----------------------------+----------------------+
| displayName                | name                 |
+----------------------------+----------------------+
| employeeId                 | employee_id          |
+----------------------------+----------------------+
| givenName                  | given_name           |
+----------------------------+----------------------+
| jobTitle                   | job_title            |
+----------------------------+----------------------+
| mail                       | email                |
+----------------------------+----------------------+
| mailNickname               | user_nickname        |
+----------------------------+----------------------+
| manager                    | manager              |
+----------------------------+----------------------+
| mobilePhone                | mobile_phone         |
+----------------------------+----------------------+
| onPremisesDistinguishedName| distinguished_name   |
+----------------------------+----------------------+
| officeLocation             | office_location      |
+----------------------------+----------------------+
| postalCode                 | postal_code          |
+----------------------------+----------------------+
| preferredLanguage          | preferred_language   |
+----------------------------+----------------------+
| state                      | state                |
+----------------------------+----------------------+
| streetAddress              | street_address       |
+----------------------------+----------------------+
| surname                    | surname              |
+----------------------------+----------------------+
| usageLocation              | usage_location       |
+----------------------------+----------------------+
| userPrincipalName          | user_principal_name  |
+----------------------------+----------------------+
| userType                   | user_type            |
+----------------------------+----------------------+


Group Fields

+---------------------+----------------------+
|   Azure AD Field    |     NEXT Field       |
+=====================+======================+
| id                  | role_id              |
+---------------------+----------------------+
| createdDateTime     | created_date         |
+---------------------+----------------------+
| deletedDateTime     | deleted_date         |
+---------------------+----------------------+
| description         | description          |
+---------------------+----------------------+
| displayName         | name                 |
+---------------------+----------------------+
| groupTypes          | group_types          |
+---------------------+----------------------+
| mailNickname        | group_nickname       |
+---------------------+----------------------+
| members             | members              |
+---------------------+----------------------+
| classification      | classification       |
+---------------------+----------------------+
| mailEnabled         | mail_enabled         |
+---------------------+----------------------+
| securityEnabled     | security_enabled     |
+---------------------+----------------------+
| owners              | owners               |
+---------------------+----------------------+
| visibility          | visibility           |
+---------------------+----------------------+
