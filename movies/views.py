import json

from aiohttp import web
from django_aiohttp import views
from django.apps import apps
from django.shortcuts import render
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django_aiohttp.utils import database_sync_to_async

routes = web.RouteTableDef()

class MovieAbstractView(views.ModelMixin):
    model = 'movies.Movie'

@routes.view('/movies')
class MoviesListView(MovieAbstractView, web.View):
    
    async def get(self):
        queryset = await self.get_queryset()
        text = serialize('json', queryset)
        return web.json_response(text=text)

@routes.view('/movies/{id}')
class MoviesDetailView(MovieAbstractView, web.View):
    
    async def get(self):
        try:
            pk = int(self.request.match_info['id'])
        except Exception as ex:
            pk = None
        finally:
            queryset = await self.get_queryset(pk=pk)
            movie = queryset.values().first()
            
            if not movie:
                return web.json_response(data={'message': 'Not found'}, status=404)
        
            text = json.dumps(movie, cls=DjangoJSONEncoder)
            return web.json_response(text=text)
            