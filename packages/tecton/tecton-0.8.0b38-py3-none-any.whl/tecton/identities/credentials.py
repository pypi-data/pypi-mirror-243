import sys
import urllib
from typing import Optional
from typing import Union

import attrs
import requests

from tecton._internals import metadata_service
from tecton._internals.utils import cluster_url
from tecton.cli import printer
from tecton.cli import workspace
from tecton.cli.workspace_utils import switch_to_workspace
from tecton.identities import api_keys
from tecton.identities import okta
from tecton_core import conf
from tecton_core import errors
from tecton_core.id_helper import IdHelper
from tecton_proto.auth.authorization_service_pb2 import GetIsAuthorizedRequest
from tecton_proto.auth.authorization_service_pb2 import Permission
from tecton_proto.auth.principal_pb2 import PrincipalType
from tecton_proto.auth.resource_pb2 import ResourceType


@attrs.frozen
class ServiceAccountProfile:
    id: str
    name: str
    description: str
    created_by: str
    is_active: bool
    obscured_key: str


# no @sdk_public_method (it throws an exception if API_SERVICE is wrong. probably requires fixing)
def set_credentials(tecton_api_key: Optional[str] = None, tecton_url: Optional[str] = None) -> None:
    """Explicitly override tecton credentials settings.

    Typically, Tecton credentials are set in environment variables, but you can
    use this function to set the Tecton API Key and URL during an interactive Python session.

    :param tecton_api_key: Tecton API Key
    :param tecton_url: Tecton API URL
    """
    if tecton_api_key:
        conf.set("TECTON_API_KEY", tecton_api_key)
    if tecton_url:
        conf.validate_api_service_url(tecton_url)
        conf.set("API_SERVICE", tecton_url)
    print("✅ Successfully set credentials.")


def clear_credentials() -> None:
    """Clears credentials set by 'set_credentials' and 'login' (clearing any locally saved Tecton API key, user token and Tecton URL)"""
    for key in (
        "TECTON_API_KEY",
        "API_SERVICE",
        "OAUTH_ACCESS_TOKEN",
        "OAUTH_REFRESH_TOKEN",
        "OAUTH_ACCESS_TOKEN_EXPIRATION",
    ):
        try:
            conf.unset(key)
        except KeyError:
            pass
    print("✅ Successfully cleared Service Account API key and User credentials from session")
    if conf.get_or_none("TECTON_API_KEY") is not None:
        print(
            "👉️ TECTON_API_KEY is still set in an environment variable or in a Secret Manager, so that credential will still be used until it is cleared."
        )


def test_credentials() -> None:
    """Test credentials and throw an exception if unauthenticated."""
    # First, check if a Tecton URL is configured.
    tecton_url = conf.tecton_url()

    # Next, determine how the user is authenticated (Okta or Service Account).
    profile = who_am_i()
    if isinstance(profile, ServiceAccountProfile):
        auth_mode = f"Service Account {profile.id} ({profile.name})"
    elif isinstance(profile, okta.UserProfile):
        auth_mode = f"User Profile {profile.email}"
    else:
        # profile can be None if TECTON_API_KEY or OAUTH_ACCESS_TOKEN is set, but invalid.
        if conf.get_or_none("TECTON_API_KEY"):
            msg = f"Invalid TECTON_API_KEY configured for {tecton_url}. Please update TECTON_API_KEY or use tecton.set_credentials(tecton_api_key=<key>)."
            raise errors.TectonAPIInaccessibleError(msg)
        elif conf.get_or_none("OAUTH_ACCESS_TOKEN"):
            msg = f"Invalid or expired user credentials for {tecton_url}. Please try tecton.login(url=<tecton_url>) again."
            raise errors.TectonAPIInaccessibleError(msg)
        msg = f"No user profile or service account configured for {tecton_url}. To authenticate using an API key, set TECTON_API_KEY in your environment or use tecton.set_credentials(tecton_api_key=<key>). To authenticate as your user, run `tecton login` with the CLI or `tecton.login(url=<url>)` in your notebook."
        raise errors.FailedPreconditionError(msg)

    print(f"Successfully authenticated to {tecton_url} using {auth_mode}.")


def who_am_i() -> Optional[Union[ServiceAccountProfile, okta.UserProfile]]:
    """Introspect the current User or API Key used to authenticate with Tecton.

    Returns:
      The UserProfile or ServiceAccountProfile of the current User or API Key (respectively) if the introspection is
      successful, else None.

    Throws:
      Permission Error if the Okta refresh token has expired.
    """
    print(f"Tecton Endpoint {cluster_url()}")

    user_profile = okta.get_user_profile()
    if user_profile:
        user_is_on_cluster = _check_user_can_read_org(user_profile.id)
        if user_is_on_cluster:
            return user_profile
        else:
            print("Unable to authenticate using the configured user credentials.")
            return None
    else:
        token = conf.get_or_none("TECTON_API_KEY")
        if token:
            try:
                introspect_result = api_keys.introspect(token)
            except PermissionError:
                print("Permissions error when introspecting the Tecton API key. The API key is invalid.")
                return None
            if introspect_result is not None:
                return ServiceAccountProfile(
                    id=IdHelper.to_string(introspect_result.id),
                    name=introspect_result.name,
                    description=introspect_result.description,
                    created_by=introspect_result.created_by,
                    is_active=introspect_result.active,
                    obscured_key=f"****{token[-4:]}",
                )

    return None


def _check_user_can_read_org(user_id: str) -> bool:
    request = GetIsAuthorizedRequest(
        principal_type=PrincipalType.PRINCIPAL_TYPE_USER,
        principal_id=user_id,
        permissions=[
            Permission(
                resource_type=ResourceType.RESOURCE_TYPE_ORGANIZATION,
                action="read_organization",
            )
        ],
    )
    try:
        response = metadata_service.instance().GetIsAuthorized(request)
    except PermissionError as e:
        # if the user doesn't exist in SpiceDB, it will say resource not found
        return False
    return len(response.permissions) > 0 and response.permissions[0].action == "read_organization"


def login(url: str) -> None:
    """
    Authenticate as a user to a Tecton instance.

    :param url: HTTP URL of the Tecton instance, e.g. https://xyz.tecton.ai
    """
    user_profile = None
    try:
        user_profile = okta.get_user_profile()
    except PermissionError as e:
        print("Re-authenticating. Previous credentials no longer valid.")
    if user_profile:
        cluster_url = conf.get_or_none("API_SERVICE")
        print(
            f"Already logged in to {cluster_url} as {user_profile}. To switch users, run `tecton.logout` then `tecton.login`"
        )
        return
    # use BROWSER_MANUAL for now, can always make it nicer later
    _login_helper(url, okta.AuthFlowType.BROWSER_MANUAL)
    printer.safe_print("✅ Authentication successful!")


def logout() -> None:
    """
    Log out of the current user session that was previously authenticated using tecton.login().
    If there is no active user session, this is a no-op.
    """
    conf.delete_okta_tokens()
    printer.safe_print("✅ Logged out of user session. Use `tecton.login()` to re-authenticate.")


def _login_helper(
    host: str,
    auth_flow_type: okta.AuthFlowType,
    okta_session_token: Optional[str] = None,
):
    """
    Common implementation for CLI `tecton login` and Notebook SDK `tecton.login()`.

    Only exits successfully on successful authentication.

    :param url: URL of Tecton deployment, e.g. https://staging.tecton.ai
    :param auth_flow_type: okta.AuthFlowType (browser, manual, or session token)
    :param okta_session_token: Optional string for auth_flow_type SESSION_TOKEN.
    """
    try:
        urllib.parse.urlparse(host)
    except Exception:
        printer.safe_print("Tecton Cluster URL must be a valid URL")
        sys.exit(1)
    # add this check for now since it can be hard to debug if you don't specify https and API_SERVICE fails
    if host is None or not (host.startswith(("https://", "http://localhost:"))):
        if host is not None and "//" not in host:
            host = f"https://{host}"
        else:
            printer.safe_print("Tecton Cluster URL must start with https://")
            sys.exit(1)

    login_configs_url = urllib.parse.urljoin(host, "api/v1/metadata-service/get-login-configs")
    try:
        response = requests.post(login_configs_url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(e)
    configs = response.json()["key_values"]
    cli_client_id = configs["OKTA_CLI_CLIENT_ID"]

    flow = okta.OktaAuthorizationFlow(auth_flow_type=auth_flow_type, okta_session_token=okta_session_token)
    auth_code, code_verifier, redirect_uri = flow.get_authorization_code(cli_client_id)
    access_token, _, refresh_token, access_token_expiration = flow.get_tokens(
        auth_code, code_verifier, redirect_uri, cli_client_id
    )
    if not access_token:
        printer.safe_print("Unable to obtain Tecton credentials")
        sys.exit(1)

    # when switching clusters
    if conf.get_or_none("API_SERVICE") != urllib.parse.urljoin(host, "api"):
        if conf.save_tecton_configs_enabled:
            # in the CLI, switch current workspace to prod
            switch_to_workspace(workspace.PROD_WORKSPACE_NAME)
        else:
            # in notebooks, clear MDS conf values from previous cluster
            conf._clear_metadata_server_config()

    new_api_service = urllib.parse.urljoin(host, "api")
    alpha_snowflake_compute_enabled = (
        configs["ALPHA_SNOWFLAKE_COMPUTE_ENABLED"] if "ALPHA_SNOWFLAKE_COMPUTE_ENABLED" in configs else False
    )
    conf.set_login_configs(
        cli_client_id=cli_client_id,
        api_service=new_api_service,
        feature_service=new_api_service,
        alpha_snowflake_compute_enabled=alpha_snowflake_compute_enabled,
    )

    conf.set_okta_tokens(access_token, access_token_expiration, refresh_token)
