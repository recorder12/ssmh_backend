from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
import requests

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions



class SearchView(APIView):
    """Search API View"""
    serializer_class = serializers.SearchSerializer
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        """Return searched data"""
        serializer = self.serializer_class(data=request.data)

        # 400 error
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        keyword = serializer.validated_data.get('keyword')
        r = requests.post('https://40a2-64-98-208-143.ngrok.io/search', json = {'query' : 'Insomnia'})

        return Response({'success' : True, 'feeds' : r.json() })


        #
        # if request.user.is_authenticated:
        #     # search data part
        #
        #
        #
        #
        #     return Response({'success': True})
        # else:
        #
        #
        # # get logged user
        #
        # print(request.user.is_authenticated)
        # user = models.UserProfile.objects.get(id=request.user.id)
        # print(user.name)

        # user logged ?










class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)
