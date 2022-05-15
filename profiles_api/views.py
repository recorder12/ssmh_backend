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

from django.http import JsonResponse



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
                {"statusCode" : 400, "msg" : "Bad request error"}
            )

        query = serializer.validated_data.get('query')
        r = requests.post('http://30ec-64-98-208-143.ngrok.io/search', json = {'query' : query})
        feeds = r.json()['Data']
        # feeds = []

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


        response = JsonResponse( {"statusCode" : 200, 'msg' : 'success', 'Data' : feeds},status=200)
        response["Access-Control-Allow-Origin"] = "*"
        return response

        # return Response({"msg" : 'success', 'Data' : feeds })


class UserLikeView(APIView):
    """Update Like API View"""
    serializer_class = serializers.UserLikeSerializer
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        # 401 error
        if request.user.is_authenticated is False:
            return Response(
                {"statusCode" : 401, "msg" : "Unauthorized error"}
            )
        # 400 error
        if serializer.is_valid() is False:
            return Response(
                {"statusCode" : 400, "msg" : "Bad request error"}
            )

        new_favorite_id = serializer.validated_data.get('feed_id') # int

        if new_favorite_id is None:
            return Response(
                {"statusCode" : 400, "msg" : "Bad request error"}
            )

        user = request.user
        user_favorites = json.loads(user.favorites) if user.favorites != ""  else []

        if new_favorite_id in user_favorites:
            user_favorites.remove(new_favorite_id)
        else:
            user_favorites.append(new_favorite_id)

        user.favorites = json.dumps(user_favorites)
        user.save()

        # to do : post like change value to flask server or external DB shared with flask server

        response = JsonResponse( {"statusCode" : 200, 'msg' : 'success'},status=200)
        response["Access-Control-Allow-Origin"] = "*"
        return response
        # return Response({"statusCode" : 200, 'msg' : 'success'})


class UserVoteView(APIView):
    """Update favorites, voted API View"""
    serializer_class = serializers.UserVoteSerializer
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        # 401 error
        if request.user.is_authenticated is False:
            return Response(
                {"statusCode" : 401, "msg" : "Unauthorized error"}
            )

        # 400 error
        if serializer.is_valid() is False:
            return Response(
                {"statusCode" : 400, "msg" : "Bad request error"}
            )

        feed_id = serializer.validated_data.get('feed_id')
        vote = serializer.validated_data.get('vote')

        if feed_id is None or vote is None:
            return Response(
                {"statusCode" : 400, "msg" : "Bad request error"}
            )

        user = request.user
        user_voted = voted = json.loads(user.voted) if user.voted != "" else {}
        user_voted[str(feed_id)] = vote
        user.voted = json.dumps(user_voted)

        # to do : post vote change value to flask server or external DB shared with flask server

        user.save()

        response = JsonResponse( {"statusCode" : 200, 'msg' : 'success'},status=200)
        response["Access-Control-Allow-Origin"] = "*"
        return response

        # return Response({"statusCode" : 200, 'msg' : 'success'})


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
    permission_classes = (permissions.UpdateOwnFeed, IsAuthenticated)

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(contentContributorId=self.request.user)
