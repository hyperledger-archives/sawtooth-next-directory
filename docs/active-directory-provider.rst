=========================
Active Directory Provider
=========================

The NEXT Identity platform interacts with Active Directory Provider through three syncs:

**Initial Inbound Sync**
    The initial inbound sync pulls all user and group records from Active Directory and stores it in a queue to be imported 
    to the NEXT platform. This sync will begin when the LDAP daemon is first initialized. After a successful initial inbound
    sync, you would be able to see all your Active Directory users and groups on the NEXT platform.

..

**Delta Inbound Sync**
    The delta inbound sync pulls all user or group records from Active Directory that have been modified since the last 
    inbound sync occurred. The records will be queued and users and groups will be updated accordingly on the NEXT platform. 
    To check for users or groups that have been modified since the last sync occurred, we utilized the whenChanged field on each 
    Active Directory record. A search query will look for all records that has a whenChanged timestamp at a later date than the 
    last sync time. By default, delta inbound sync will occur by default every hour, but can be configured in the environment 
    variables (refer to the Setting up Environment Variables below for more details).

..

**Delta Outbound Sync**
    The delta outbound sync will record all changes to users and groups as they occur on the NEXT platform by storing the changes 
    in a queue. From the queue, each change will be processed and Active Directory will be updated accordingly. The delta outbound
    sync will help keep your Active Directory stay up to date with the changes that are being performed on NEXT.

Integrating Active Directory Provider and NEXT
==============================================

Setting up Environment Variables
--------------------------------
To connect your organization's Active Directory provider to the NEXT platform, you must configure the following environment variables 
in the .env file located in the root directory.

* **LDAP_DC**: The unique domain controller for your Active Directory instance 
* **LDAP_SERVER**: The IP address of the Active Directory instance containing the prefix "ldap://"
* **LDAP_USER**: The username of a user that has access to search and udpate users and groups in the Active Directory domain controller
* **LDAP_PASS**: The password used to authenticate as the LDAP_USER
* **DELTA_SYNC_INTERVAL_SECONDS**: The interval (in seconds) of when the outbound delta sync would be performed 


Example list of environment variables in .env:
    LDAP_DC=DC=test,DC=example,DC=com

    LDAP_SERVER=ldap://10.123.123.123

    LDAP_USER=ad_admin

    LDAP_PASS=ad_admin_pw

    DELTA_SYNC_INTERVAL_SECONDS=3600

Active Directory Data Field Mapping
----------------------------------------
When data is imported into the NEXT platform from Active Directory, the data field names for Active Directory users and groups will be 
mapped to new field names to allow our platform to interact with the incoming data. Active Directory data fields are currently being 
mapped according to the tables below.

User Fields

+---------------------+----------------------+
|      AD Field       |     NEXT Field       |
+=====================+======================+
| objectGUID          | next_id              |
+---------------------+----------------------+
| telephoneNumber     | business_phones      |
+---------------------+----------------------+
| whenCreated         | created_date         |
+---------------------+----------------------+
| company             | company_name         |
+---------------------+----------------------+
| countryCode         | country              |
+---------------------+----------------------+
| department          | department           |
+---------------------+----------------------+
| memberOf            | member_of            |
+---------------------+----------------------+
| displayName         | name                 |
+---------------------+----------------------+
| employeeID          | employee_id          |
+---------------------+----------------------+
| givenName           | given_name           |
+---------------------+----------------------+
| title               | job_title            |
+---------------------+----------------------+
| mail                | email                |
+---------------------+----------------------+
| cn                  | user_nickname        |
+---------------------+----------------------+
| manager             | manager              |
+---------------------+----------------------+
| mobilePhone         | mobile_phone         |
+---------------------+----------------------+
| distinguishedName   | distinguished_name   |
+---------------------+----------------------+
| postalCode          | postal_code          |
+---------------------+----------------------+
| preferredLanguage   | preferred_language   |
+---------------------+----------------------+
| streetAddress       | street_address       |
+---------------------+----------------------+
| userPrincipalName   | user_principal_name  |
+---------------------+----------------------+


Group Fields

+---------------------+----------------------+
|      AD Field       |     NEXT Field       |
+=====================+======================+
| objectGUID          | role_id              |
+---------------------+----------------------+
| whenChanged         | created_date         |
+---------------------+----------------------+
| description         | description          |
+---------------------+----------------------+
| name                | name                 |
+---------------------+----------------------+
| groupType           | group_types          |
+---------------------+----------------------+
| member              | members              |
+---------------------+----------------------+
| managedBy           | owners               |
+---------------------+----------------------+
