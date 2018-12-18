from ldap3 import Server, Connection, ALL

# Search filter options
# NOTE: User filter has a placeholder for the ${USER_ID}. It needs to be manually
#       replaced with an actual user id before usage.
search_filters = {
    'all_users': '(objectClass=person)',
    'all_groups': '(objectClass=group)',
    'specific_user': '(&(objectClass=person)(distinguishedName=CN=${USER_ID},OU=Privileged,OU=Users,OU=Accounts,DC=clouddev,DC=corporate,DC=t-mobile,DC=com))'
}

# Large collection of test data. Useful for testing load and heavier sync phases
large_org = {
    'url': 'ldap:${URL}',
    'user': '${USER}',
    'password': '${PASSWORD}',
    'domain_components': 'DC=gsmtest,DC=corporate,DC=t-mobile,DC=com',
}

# Smaller collection of test data. Useful for sorting out field mappings and making quick lookups
small_org = {
    'url': 'ldap://${URL}',
    'user': '${USER}',
    'password': '${PASSWORD}',
    'domain_components': 'DC=clouddev,DC=corporate,DC=t-mobile,DC=com'
}

# Customize the query here
org = large_org
search_filter = search_filters['all_users']
paged_size = 500

server = Server(large_org['url'], use_ssl=True, get_info=ALL)

conn = Connection(server, user=org['user'], password=org['password'], auto_bind=True)

# print('**********Server Info**********')
# print(server.info)

# print('**********Server Schema**********')
# print(server.schema)

print("Querying ldap...")

search_parameters = {'search_base': org['domain_components'],
                     'search_filter': search_filter,
                     # 'attributes': [],
                     'paged_size': paged_size}

index = 1
while True:
    conn.search(**search_parameters)
    for entry in conn.entries:
        print('Result: ' + str(index))
        print(entry)
        index = index + 1
        # 1.2.840.113556.1.4.319 is the OID/extended control for PagedResults
    cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
    if cookie:
        search_parameters['paged_cookie'] = cookie
    else:
        break
