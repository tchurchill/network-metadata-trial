from rest_framework import serializers
from django.db.models import Prefetch

import logging
from api.models import (
    Member,
    MemberProfileFulfillmentModel,
    MemberProfileFulfillmentModelRequirement,
    MemberProfile,
    MemberProfileDraft,
    MemberProfileProgram,
    MemberProfileVersion,
)


logger = logging.getLogger(__name__)


class NetworkProfileFulfillmentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MemberProfileFulfillmentModel
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class MemberProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfile
        fields = "__all__"


class MemberFulfillmentModelRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfileFulfillmentModelRequirement
        fields = "__all__"


class RetailerProgramModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = MemberProfileProgram
        fields = (
            "id",
            "name",
            "active"
        )


class RetailerNetworkProfileFulFillmentModelSerializer(serializers.ModelSerializer):
    requirements = MemberFulfillmentModelRequirementSerializer(
        source="filtered_reqs", many=True
    )
    programs = RetailerProgramModelSerializer(source="filtered_programs", many=True)

    class Meta:
        model = MemberProfileFulfillmentModel
        fields = (
            "id",
            "networkFulfillmentModel",
            "networkVertical",
            "requirements",
            "programs"
        )


class NetworkProfileDraftModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfileDraft
        fields = "__all__"


class RetailerModelSerializer(serializers.Serializer):
    fulfillmentModels = RetailerNetworkProfileFulFillmentModelSerializer(many=True)


class NetworkProfileDraftWithDataModelSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        reqs = instance.snapshot.pop("memberprofilefulfillmentmodelrequirement__id__in")
        programs = instance.snapshot.pop("memberprofileprogram__id__in")
        ffms = MemberProfileFulfillmentModel.objects.filter(**instance.snapshot)
        data_queryset = ffms.prefetch_related(
            Prefetch(
                "memberprofilefulfillmentmodelrequirement_set",
                MemberProfileFulfillmentModelRequirement.objects.filter(id__in=reqs),
                to_attr="filtered_reqs",
            ),
            Prefetch(
                "memberprofileprogram_set",
                MemberProfileProgram.objects.filter(id__in=programs),
                to_attr="filtered_programs"
            )
        )
        instance.fulfillmentModels = data_queryset
        return RetailerModelSerializer(instance).data

    class Meta:
        model = MemberProfileDraft
        fields = (
            "id",
            "name",
            "description",
            "majorVersion",
            "minorVersion",
            "data",
        )


class NetworkProfileVersionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberProfileVersion
        fields = "__all__"


class NetworkProfileVersionWithDataModelSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, instance):
        reqs = instance.snapshot.pop("memberprofilefulfillmentmodelrequirement__id__in")
        programs = instance.snapshot.pop("memberprofileprogram__id__in")
        ffms = MemberProfileFulfillmentModel.objects.filter(**instance.snapshot)
        data_queryset = ffms.prefetch_related(
            Prefetch(
                "memberprofilefulfillmentmodelrequirement_set",
                MemberProfileFulfillmentModelRequirement.objects.filter(id__in=reqs),
                to_attr="filtered_reqs",
            ),
            Prefetch(
                "memberprofileprogram_set",
                MemberProfileProgram.objects.filter(id__in=programs),
                to_attr="filtered_programs"
            )
        )
        instance.fulfillmentModels = data_queryset
        return RetailerModelSerializer(instance).data

    class Meta:
        model = MemberProfileVersion
        fields = (
            "id",
            "active",
            "name",
            "description",
            "version",
            "data",
        )