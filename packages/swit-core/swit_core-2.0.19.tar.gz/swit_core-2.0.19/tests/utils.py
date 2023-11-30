import os

from fastapi import FastAPI


def create_fastapi_app():
    os.environ["SWIT_CLIENT_ID"] = "test_client_id"
    os.environ["SWIT_CLIENT_SECRET"] = "test_client_secret"
    os.environ["SWIT_SINGING_KEY"] = "test_singing_key"
    os.environ["APPS_ID"] = "test_apps_id"
    os.environ["DB_USERNAME"] = "test_db_username"
    os.environ["DB_PASSWORD"] = "test_db_password"
    os.environ["DB_NAME"] = "test_db_name"
    os.environ["ENV_OPERATION"] = "local"
    os.environ["BASE_URL"] = "test_base_url"
    os.environ["LOCALIZE_PROJECT_ID"] = "test_localize_project_id"
    os.environ["DB_HOST"] = "test_db_host"
    os.environ[
        "SCOPES"] = ("imap:write+imap:read+user:read+message:write+channel:read+workspace:read+project"
                     ":read+project:write+task:read+task:write")
    os.environ["BOT_REDIRECT_URL"] = "/auth/callback/bot"
    os.environ["USER_REDIRECT_URL"] = "/auth/callback/user"

    return FastAPI()
