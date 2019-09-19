from aiohttp import web
from django import setup
from django.conf import settings

from django_aiohttp import settings as app_settings
from movies.routes import movies_app

async def setup_django(app):
    '''
    Configures database and installed apps so
    we can have Django ORM ready to be used.
    '''
    
    settings.configure(
       INSTALLED_APPS = app_settings.INSTALLED_APPS,
       DATABASES = app_settings.DATABASES,
       MIDDLEWARE= app_settings.MIDDLEWARE,
       AUTH_PASSWORD_VALIDATORS = app_settings.AUTH_PASSWORD_VALIDATORS,
       CORS_ORIGIN_WHITELIST= app_settings.CORS_ORIGIN_WHITELIST,
       WSGI_APPLICATION= app_settings.WSGI_APPLICATION,
    )
    setup()

app = web.Application()
app.on_startup.append(setup_django)
app.add_subapp('/api/', movies_app)

# if __name__ == "__main__":
#     web.run_app(
#         app,
#         host="0.0.0.0",
#         port=8000,
#     )