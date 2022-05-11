from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
