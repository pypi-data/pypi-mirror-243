'''A collection of functions to interact with Azure Active Directory'''
import base64
import logging
import requests
import msal
import os
import json
import jwt
import logging


from datetime import datetime


# FIXED Microsoft-dictated endpoints and parameters
graphURI = 'https://graph.microsoft.com'
scope = ['https://graph.microsoft.com/.default']

# AAD Application parameters
# when you add an AAD authentication to your function app, it will create an AAD Application
# go to its page in the Portal, edit it by adding user roles, then add the following permissions:
'''
Application.Read.All
Directory.Read.All
User.Read
User.Read.All
User.ReadBasic.All
'''
# save the whole thing (some app premissions may require approval from your AD Admin).
# Now you can fill properly the following fields
# you can take them from the APPLICATION MANIFEST file
# it looks like '32cc535d-3164-4d2c-99e4-92324ada27b3', it's the "appId" in manifest
# look into the "appRoles" object and pick "id" as key and "value" as value
def _get_client_id_from_env():
	try:
		clientID = os.environ['MICROSOFT_PROVIDER_AUTHENTICATION_CLIENT_ID']
	except KeyError:
		clientID = None
		logging.warning('[WARNING] AAD Client ID not found in environment variables, pass it explicitly with the clientID parameter')
	return clientID

# CLIENT SECRET
# you have to generate this one from the Certificates & Secretes blade. Since secrets last
# 2 years tops, let's slap it into a CONFIGURATION PARAMETER so you won't have to re-deploy
# the function app every fucking time the little motherfucker expires.
def _get_client_secret_from_env():
	try:
		clientSecret = os.environ['MICROSOFT_PROVIDER_AUTHENTICATION_SECRET']
	except KeyError:
		clientSecret = None
		logging.warning('[WARNING] AAD Client secret not found in environment variables, pass it explicitly with the clientSecret parameter')
	return clientSecret

# this is a rat bastard https://stackoverflow.com/questions/37151346/authorization-identitynotfound-error-while-accessing-graph-api
# it looks like this '94dc0eeb-2c10-4dbf-a033-c0683ba0eec9' 
# you find this in the Overvew blade in the AAD application
def _get_tenant_ID_from_env():
	try:
		tenantID = os.environ['MICROSOFT_PROVIDER_AUTHENTICATION_TENANT_ID']
	except KeyError:
		tenantID = None
		logging.warning('[WARNING] AAD Tenant ID not found in environment variables, pass it explicitly with the tenantID parameter')
	return tenantID

# ENTERPRISE APPLICATION parameters
# now move to the Enterpise Application object (is should have the same name as the AAD application and it
# should be accessible from the "overview" blade in the AAD application)
# its ID looks like this '12da6679-c0d1-43fe-9c29-56965dffadf2'
# and its hideous!
def _get_object_id_from_env():
	try:
		object_id = os.environ['MICROSOFT_PROVIDER_AUTHENTICATION_APPLICATION_OBJECT_ID']
	except KeyError:
		object_id = None
		logging.warning('[WARNING] AAD Enterprise Application ID not found in environment variables, pass it explicitly with the object_id parameter')
	return object_id

# HANDLING AUTHENTICATION
def msgraph_auth(
	clientID = None,
	clientSecret = None,
	tenantID = None,
	base_authority = 'https://login.microsoftonline.com/'):
    '''gets an appropriate request header to include in all subsequent AAD requests.
	It includes some caching, so feel free to call as many times as you like'''
    if clientID is None:
        clientID = _get_client_id_from_env()
    if clientSecret is None:
        clientSecret = _get_client_secret_from_env()
    if tenantID is None:
        tenantID = _get_tenant_ID_from_env()
    authority = base_authority + tenantID
    app = msal.ConfidentialClientApplication(clientID, authority=authority, client_credential = clientSecret)
    try:
        accessToken = app.acquire_token_silent(scope, account=None)
        if not accessToken:
            try:
                accessToken = app.acquire_token_for_client(scopes=scope)
                if accessToken['access_token']:
                    print('New access token retreived')
                    requestHeaders = {'Authorization': 'Bearer ' + accessToken['access_token']}
                else:
                    print('Error aquiring authorization token. Check your tenantID, clientID and clientSecret.')
            except:
                pass 
        else:
            print('Token retreived from MSAL Cache')
            requestHeaders = {'Authorization': 'Bearer ' + accessToken['access_token']}
        return requestHeaders
    except Exception as err:
        print(err)

# QUERYING MS GRAPH
def msgraph_request(resource,requestHeaders = None, **kwargs):
	# Request
	if requestHeaders is None:
		requestHeaders = msgraph_auth(**kwargs)
	results = requests.get(resource, headers=requestHeaders).json()
	return results

# QUERY FORMATTING METHODS
# get a user's information
# AAD REST API https://docs.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0&tabs=http
def get_user_anagraphics(uid, requestHeaders = None, **kwargs):
	request_url = 'https://graph.microsoft.com/v1.0/users/'+str(uid)
	return msgraph_request(request_url, requestHeaders, **kwargs)

def get_user_application_roles(uid, requestHeaders=None, **kwargs):
	request_url = 'https://graph.microsoft.com/v1.0/users/' + str(uid)+ '/appRoleAssignments'
	return msgraph_request(request_url, requestHeaders, **kwargs)

def get_users(requestHeaders = None, **kwargs):
	request_url = 'https://graph.microsoft.com/v1.0/users/'
	return msgraph_request(request_url, requestHeaders, **kwargs)

def get_application_users(requestHeaders = None, object_id = None , **kwargs):
    if object_id is None:
        object_id = _get_object_id_from_env()
    request_url = 'https://graph.microsoft.com/v1.0/servicePrincipals/'+ object_id +'/appRoleAssignedTo'
    return msgraph_request(request_url, requestHeaders, **kwargs)
# fetches objects like this
#{
# 'id': 'MLDDJlTnckqtOAx9HxAwnEdirTTyNfNKtnlr0vQ4RCw', 
# 'deletedDateTime': None, 
# 'appRoleId': 'd1717ff7-5dcf-4548-b8d8-80873b25c819', 
# 'createdDateTime': '2021-10-25T09:31:32.6833212Z', 
# 'principalDisplayName': 'dario de nart', 
# 'principalId': '26c3b030-e754-4a72-ad38-0c7d1f10309c', 
# 'principalType': 'User', 
# 'resourceDisplayName': 'crea-bee-hive-management-backend', 
# 'resourceId': '12da6679-c0d1-43fe-9c29-56965dffadf2'
# }


### FINALLY: getting the user's data from authentication

def read_user_authorization(request, **kwargs):
	'''Get user data from the http request object'''
	try:
		return read_user_from_jwt(request, **kwargs)
	except AuthorizationError as ae:
		try: 
			return parse_client_principal(request.headers['x-ms-client-principal'])
		except KeyError as ke:
			# no client principal at all, let's show to the client the JWT authentication error
			raise ae
		except  Exception as e:
			# there is a client principal, hence we show the client principal parsing error
			raise AuthorizationError({"code": 'Bad client principal',"description": str(e)}, code = 401)

# https://docs.microsoft.com/en-us/azure/active-directory/develop/scenario-daemon-acquire-token?tabs=python#acquiretokenforclient-api
'''
POST /{tenant}/oauth2/v2.0/token HTTP/1.1           //Line breaks for clarity
Host: login.microsoftonline.com
Content-Type: application/x-www-form-urlencoded

client_id=535fb089-9ff3-47b6-9bfb-4f1264799865
&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default
&client_secret=sampleCredentia1s
&grant_type=client_credentials
'''
# https://blog.darrenjrobinson.com/microsoft-graph-using-msal-with-python/

def parse_client_principal(principal):
	'''given the b64 representation of the client principal, this function
	returns a dictionary with the relevant information'''
	cp_dict =  json.loads(base64.b64decode(principal).decode("utf-8"))
	if cp_dict['auth_typ'] == 'aad':
		claim_dict ={}
		for claim in cp_dict['claims']:
			claim_dict[claim['typ']] = claim['val']
		# now 
		return {
			'uid': claim_dict.get('http://schemas.microsoft.com/identity/claims/objectidentifier'),
			'name' :claim_dict.get('preferred_username'),
			'display_name' : claim_dict.get('name'),
			'email' : claim_dict.get('http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress'),
			'role' : claim_dict.get('roles')
		}
	return None


def read_user_from_jwt(request, **kwargs):
	'''reads the JWT object from client request'''
	token = get_token_auth_header(request)
	decoded = jwt.decode(token, options={"verify_signature": False})
	return get_user_anagraphics(decoded.get("oid"), **kwargs)



def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthorizationError({"code": "authorization_header_missing",
                        "description":
                            "Authorization header is expected"}, 401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthorizationError({"code": "invalid_header",
                        "description":
                            "Authorization header must start with"
                            " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthorizationError({"code": "invalid_header",
                        "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthorizationError({"code": "invalid_header",
                        "description":
                            "Authorization header must be"
                            " Bearer token"}, 401)

    token = parts[1]
    #print(token)
    #logging.info(str(token))
    return token

class AuthorizationError(Exception):
	'''autorization error to show in case of user auth clusterfuck'''
	def __init__(self, message, code):
		self.message=message
		self.code = code