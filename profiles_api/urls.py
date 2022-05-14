

from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views


router = DefaultRouter()
# router.register('search', views.SearchViewSet, base_name='search')
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('search/', views.SearchView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('like/', views.UserLikeView.as_view()),
    path('vote/', views.UserVoteView.as_view()),
    path('', include(router.urls))
]
