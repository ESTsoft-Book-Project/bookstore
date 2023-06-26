from core.env import config
import dj_database_url


DATABASE_URL= config("DATABASE_URL", default=None)

if DATABASE_URL is not None:
    DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True
    )
}