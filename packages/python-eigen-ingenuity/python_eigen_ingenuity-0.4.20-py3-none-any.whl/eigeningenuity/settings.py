import os
from getpass import getuser

_token_cache_enabled_ = True
_azure_auth_enabled_ = True
_azure_tenant_id_ = os.getenv("TENANTID", "74efa022-e6d6-42ad-bc15-edc76c525bde")
_azure_client_id_ = os.getenv("CLIENTID", "c2b9aa13-e178-4dde-bc2c-b6cc4c8391d2")

def clear_token_cache():
    """
    Delete any cached tokens for the current signed in user

    Args:
        None

    Returns:
        None
    """
    if os.path.exists(os.path.dirname(__file__) + f'/.azure/{getuser()}_cache.bin'):
        os.remove(os.path.dirname(__file__) + f'/.azure/{getuser()}_cache.bin')

def disable_token_cache(state=True):
    """
    Prevent the program from creating/using/updating the token cache when authenticating with Azure. Note that this will not delete any existing tokens, for this see clear_token_cache()

    Args:
        None

    Returns:
        None
    """
    global _token_cache_enabled_
    _token_cache_enabled_ = not state

def disable_azure_auth(state=True):
    """
    Skip all azure authentication steps, note that this will cause an error if querying a protected resource

    Args:
        None

    Returns:
        None
    """
    global _azure_auth_enabled_
    _azure_auth_enabled_ = not state

def set_azure_tenant_id(id):
    """
    Set the ID of the Azure tenant of the eigenserver. This value is required for Azure authentication, but the use of the TENANTID environmental variable can be used as an alternative way of setting it.

    Args:
        id: The ID of your tenant in Azure. This can be found at portal.azure.com.

    Returns:
        None
    """
    global _azure_tenant_id_
    _azure_tenant_id_ = id

def set_azure_client_id(id):
    """
    Set the Client ID of the App registration for the eigenserver. This value required for Azure authentication, but the use of the CLIENTID environmental variable can be used as an alternative way of setting it.

    Args:
        id: The ID of your tenant in Azure. This can be found at portal.azure.com.

    Returns:
        None
    """
    global _azure_client_id_
    _azure_client_id_ = id
