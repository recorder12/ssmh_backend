from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from profiles_api import serializers


class HelloApiView(APIView):
    """ Test API View """
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """ Returns a list of APIView features """
        an_apiview = [
            'Uses HTTP methodas as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
        ]

        return Response({'messages' : 'API views', 'an_apiview' : an_apiview})

    def post(self, request):
        """ Create a hello message with our name """
        serializer = self.serializer_class(data=request.data) # json to data

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message' : message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """ Handle updating ad object """
        return Response({'method' : 'PUT'})

    def patch(self, request, pk=None):
        """ HAdle partial update of an object """
        return Response({'method' : 'PATCH'})

    def delete(self, request, pk=None):
        """ Delete an object """
        return Response({'method' : 'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """ Test API ViewSet """
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """ Return a hello message """
        a_viewset = [
            'Uses actios (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality iwth less code'
        ]

        return Response({'message' : 'Hello!', 'a_viewset' : a_viewset})

    def create(self, request):
        """ Create a new hello message """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message' : message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def retrieve(self, request, pk=None):
        """ Handle getting an object by its """
        return Response({'http_method' : 'GET'})

    def update(self, request, pk=None):
        """ Handle updating an object """
        return Response({'http_method' : 'PUT'})

    def partial_update(self, request, pk=None):
        """ Handle updating part of an object """
        return Response({'http_method' : 'PATCH'})

    def destroy(self, request, pk=None):
        """ Handle removing an object """
        return Response({'http_method' : 'DELETE'})
