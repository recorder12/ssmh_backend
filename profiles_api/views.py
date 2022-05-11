from rest_framework.views import APIView
from rest_framework.response import Response


class HelloApiView(APIView):
    """ Test API View """

    def get(self, request, format=None):
        """ Returns a list of APIView features """
        an_apiview = [
            'Uses HTTP methodas as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
        ]

        return Response({'messages' : 'API views', 'an_apiview' : an_apiview})
