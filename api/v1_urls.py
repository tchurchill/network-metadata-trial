from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from api.views import (
    MemberProfileViewSet,
    MemberViewSet,
    MemberProfileDraftViewSet,
    MemberProfileVersionViewSet,
    FulfillmentModelViewSet
)

router = DefaultRouter()
router.register("members", MemberViewSet, basename="members")
router.register("fulfillment-models", FulfillmentModelViewSet, basename="fulfillment-models")
member_router = routers.NestedSimpleRouter(router, "members", lookup="members")
member_router.register(
    "profiles", MemberProfileViewSet, basename="member-profiles"
)
profile_router = routers.NestedSimpleRouter(
    member_router, "profiles", lookup="profiles"
)
profile_router.register(
    "drafts", MemberProfileDraftViewSet, basename="profile-drafts"
)
profile_router.register(
    "versions", MemberProfileVersionViewSet, basename="profile-versions"
)
urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(member_router.urls)),
    path(r"", include(profile_router.urls)),
]
