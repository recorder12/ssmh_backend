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
import json
import ast

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

        query = serializer.validated_data.get('query')
        r = requests.post('https://40a2-64-98-208-143.ngrok.io/search', json = {'query' : query})
        feeds = r.json()['Data']

        if request.user.is_authenticated:
            user = request.user
            favorites = user.favorites
            voted = user.voted

            if favorites:
                favorites = json.loads(favorites) if favorites != "" else [] # string to list
                for obj in feeds:
                    if obj['id'] in favorites:
                        obj['favorite'] = 1

            if voted:
                voted = json.loads(voted) if voted != "" else {} # string to json
                print(voted)
                for obj in feeds:
                    if str(obj['id']) in list(voted.keys()):
                        obj['voted'] = voted[str(obj['id'])]

        return Response({'success' : True, 'Data' : feeds })


class UserLikeView(APIView):
    """Update Like API View"""
    serializer_class = serializers.UserLikeSerializer
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        # 401 error
        if request.user.is_authenticated is False:
            return Response(
                serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED
            )
        # 400 error
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


        new_favorite_id = serializer.validated_data.get('feed_id') # int

        if new_favorite_id is None:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user_favorites = json.loads(user.favorites) if user.favorites != ""  else []

        if new_favorite_id in user_favorites:
            user_favorites.remove(new_favorite_id)
        else:
            user_favorites.append(new_favorite_id)

        user.favorites = json.dumps(user_favorites)
        user.save()

        return Response({'msg' : 'success'})


class UserVoteView(APIView):
    """Update favorites, voted API View"""
    serializer_class = serializers.UserVoteSerializer
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        # 401 error
        if request.user.is_authenticated is False:
            return Response(
                serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED
            )

        # 400 error
        if serializer.is_valid() is False:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        feed_id = serializer.validated_data.get('feed_id')
        vote = serializer.validated_data.get('vote')

        if feed_id is None or vote is None:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        user_voted = voted = json.loads(user.voted) if user.voted != "" else {}
        user_voted[str(feed_id)] = vote
        user.voted = json.dumps(user_voted)
        user.save()

        return Response({'msg' : 'success'})



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
