import logging
from django.db.models import Prefetch
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from api.models import (
    MemberProfileProgram,
    MemberProfileVersion,
    NetworkFulfillmentModel,
    Member,
    MemberProfileDraft,
    MemberProfileFulfillmentModel,
    MemberProfileFulfillmentModelRequirement,
    MemberProfile,
    NetworkVertical,
    RequirementType,
    MemberProfileFulfillmentModel
)
from api.serializers import (
    MemberSerializer,
    MemberProfileSerializer,
    NetworkProfileDraftModelSerializer,
    NetworkProfileDraftWithDataModelSerializer,
    NetworkProfileVersionModelSerializer,
    NetworkProfileVersionWithDataModelSerializer,
    NetworkProfileFulfillmentModelSerializer
)

logger = logging.getLogger(__name__)


class FulfillmentModelViewSet(viewsets.ModelViewSet):
    queryset = MemberProfileFulfillmentModel.objects.filter(active=True)
    serializer_class = NetworkProfileFulfillmentModelSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request):
        member = Member.objects.create(organizationId=request.data["organizationId"])
        return Response(self.serializer_class(member).data)


class MemberProfileViewSet(viewsets.ModelViewSet):
    queryset = MemberProfile.objects.all()
    serializer_class = MemberProfileSerializer

    def create(self, request, members_pk):
        member_profile = MemberProfile.objects.create(
            profileType_id=request.data["profileType"], member_id=members_pk
        )
        return Response(self.serializer_class(member_profile).data)


class MemberProfileDraftViewSet(viewsets.ModelViewSet):
    queryset = MemberProfileDraft.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NetworkProfileDraftWithDataModelSerializer
        return NetworkProfileDraftModelSerializer

    def create(self, request, members_pk, profiles_pk):
        # FFMs #
        with transaction.atomic():
            ffms = []
            reqs = []
            programs = []
            fulfillment_models = request.data["fulfillmentModels"]
            for ffm in fulfillment_models:
                name = ffm["fulfillmentModel"]
                ffm_vertical = ffm["vertical"]
                requirements = ffm["requirements"]
                request_programs = ffm["programs"]
                network_ffm = NetworkFulfillmentModel.objects.get(name=name)
                network_vertical = (
                    NetworkVertical.objects.get(name=ffm_vertical)
                    if ffm_vertical
                    else None
                )
                ffm = MemberProfileFulfillmentModel.objects.get_or_create(
                    memberProfile_id=profiles_pk,
                    networkFulfillmentModel=network_ffm,
                    networkVertical=network_vertical,
                )
                ffms.append(ffm[0])
                for req in requirements:
                    req_type = RequirementType.objects.get(name=req["requirementType"])
                    req_model = (
                        MemberProfileFulfillmentModelRequirement.objects.get_or_create(
                            requirementType=req_type,
                            memberProfileFulfillmentModel=ffm[0],
                            detail=req["detail"],
                        )
                    )
                    reqs.append(req_model[0])
                
                for program in request_programs:
                    p = MemberProfileProgram.objects.create(
                        name=program['name'],
                        memberProfileFulfillmentModel=ffm[0]
                    )
                    programs.append(p)
            draft = MemberProfileDraft.objects.create(
                memberProfile_id=profiles_pk,
                name=request.data['name'],
                description=request.data['description'],
                majorVersion=request.data['majorVersion'],  # this needs to be calculated
                minorVersion=request.data['minorVersion'],  # same
                snapshot={
                    "id__in": [ffm.id for ffm in ffms],
                    "memberprofilefulfillmentmodelrequirement__id__in": [
                        req.id for req in reqs
                    ],
                    "memberprofileprogram__id__in": [p.id for p in programs]
                },
            )
            serializer = self.get_serializer_class()
            return Response(serializer(draft).data)


class MemberProfileVersionViewSet(viewsets.ModelViewSet):
    queryset = MemberProfileVersion.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return NetworkProfileVersionWithDataModelSerializer
        return NetworkProfileVersionModelSerializer

    def create(self, request, members_pk, profiles_pk):
        # FFMs #
        with transaction.atomic():
            # get provided draft maybe? #
            draft = MemberProfileDraft.objects.get(id=request.data['draftId'])
            version = MemberProfileVersion.objects.create(
                memberProfile_id=profiles_pk,
                name=request.data['name'],
                description=request.data['description'],
                version=draft.majorVersion,  # figure this out
                snapshot=draft.snapshot,
                active=True
            )

            # need to update all things to active here #
            # this is kinda annoying #
            reqs = version.snapshot.pop("memberprofilefulfillmentmodelrequirement__id__in")
            req_models = MemberProfileFulfillmentModelRequirement.objects.filter(id__in=reqs)
            for req in req_models:
                req.active = True
                req.save()
            programs = version.snapshot.pop("memberprofileprogram__id__in")
            program_models = MemberProfileProgram.objects.filter(id__in=programs)
            for program in program_models:
                program.active = True
                program.save()
            ffms = MemberProfileFulfillmentModel.objects.filter(**version.snapshot)
            for ffm in ffms:
                ffm.active = True
                ffm.save()
            serializer = self.get_serializer_class()
            return Response(serializer(version).data)