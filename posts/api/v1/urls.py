from django.urls import path
from rest_framework import routers

from posts.api.v1.views import (
    PostViewSet,
    LikeViewSet,
    AnalyticView,
    UserActivityView,
    SignUpUserView,
)

router = routers.SimpleRouter()
router.register(r"posts", PostViewSet, basename="posts")
router.register(r"likes", LikeViewSet, basename="likes")

urlpatterns = [
    path("analytics/", AnalyticView.as_view(), name="analytic"),
    path("user-activity/<int:pk>/", UserActivityView.as_view(), name="user-activity"),
    path("sign-up/", SignUpUserView.as_view(), name="sign-up"),
]

urlpatterns += router.urls
