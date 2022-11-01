from django.db import models
from enum import Enum
from simple_history.models import HistoricalRecords


class NetworkMemberProfileTypes(Enum):
    RETAILER = "RETAILER"
    THIRD_PARTY_LOGISTICS = "3PL"


class ReqTypes(models.TextChoices):
    GENERAL_NOTE = "GENERAL_NOTE"


class RequirementType(models.Model):
    name: models.CharField = models.CharField(
        max_length=50, choices=ReqTypes.choices, unique=True
    )


class NetworkMemberProfileType(models.Model):
    name: models.CharField = models.CharField(
        max_length=50,
        choices=[(status, status.value) for status in NetworkMemberProfileTypes],
    )


class NetworkFulfillmentModel(models.Model):
    name: models.CharField = models.CharField(max_length=256, unique=True)
    definition: models.CharField = models.CharField(max_length=256)


class NetworkVertical(models.Model):
    name: models.CharField = models.CharField(max_length=256, unique=True)
    definition: models.CharField = models.CharField(max_length=256)


class Member(models.Model):
    organizationId: models.CharField = models.CharField(max_length=50, unique=True)


class MemberProfile(models.Model):
    profileType: models.ForeignKey = models.ForeignKey(
        NetworkMemberProfileType, on_delete=models.CASCADE
    )
    member: models.ForeignKey = models.ForeignKey(
        Member, on_delete=models.CASCADE
    )


class MemberProfileFulfillmentModel(models.Model):
    memberProfile: models.ForeignKey = models.ForeignKey(
        MemberProfile, on_delete=models.CASCADE
    )
    networkFulfillmentModel: models.ForeignKey = models.ForeignKey(
        NetworkFulfillmentModel, on_delete=models.CASCADE
    )
    networkVertical: models.ForeignKey = models.ForeignKey(
        NetworkVertical, on_delete=models.CASCADE, null=True, blank=True
    )
    # i think we want this on the entity b/c of filtering the network #
    active: models.BooleanField = models.BooleanField(default=False)


class MemberProfileProgram(models.Model):
    name: models.CharField = models.CharField(max_length=256)
    active: models.BooleanField = models.BooleanField(default=False)
    memberProfileFulfillmentModel: models.ForeignKey = models.ForeignKey(
        MemberProfileFulfillmentModel, on_delete=models.CASCADE
    )


class MemberProfileFulfillmentModelRequirement(models.Model):
    requirementType: models.ForeignKey = models.ForeignKey(
        RequirementType, on_delete=models.CASCADE
    )
    memberProfileFulfillmentModel: models.ForeignKey = models.ForeignKey(
        MemberProfileFulfillmentModel, on_delete=models.CASCADE
    )
    detail: models.JSONField = models.JSONField(max_length=1024)
    # i think we want this on the entity b/c of filtering the network #
    active: models.BooleanField = models.BooleanField(default=False)


class MemberProfileVersion(models.Model):
    memberProfile: models.ForeignKey = models.ForeignKey(
        MemberProfile, on_delete=models.CASCADE
    )
    active: models.BooleanField = models.BooleanField(default=False)
    name: models.CharField = models.CharField(max_length=100)
    description: models.CharField = models.CharField(max_length=256)
    createdDate: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    createdBy: models.CharField = models.CharField(max_length=256)
    version: models.CharField = models.CharField(max_length=4)
    snapshot: models.JSONField = models.JSONField(max_length=1024)


class MemberProfileDraft(models.Model):
    memberProfile: models.ForeignKey = models.ForeignKey(
        MemberProfile, on_delete=models.CASCADE
    )
    name: models.CharField = models.CharField(max_length=100)
    description: models.CharField = models.CharField(max_length=256)
    createdDate: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    createdBy: models.CharField = models.CharField(max_length=256)
    majorVersion: models.CharField = models.CharField(max_length=4)
    minorVersion: models.CharField = models.CharField(max_length=4)
    snapshot: models.JSONField = models.JSONField(max_length=1024)
