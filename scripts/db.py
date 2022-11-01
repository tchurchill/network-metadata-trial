from api.models import (
    NetworkFulfillmentModel,
    NetworkVertical,
    RequirementType,
    Member,
    MemberProfile,
    NetworkMemberProfileType,
)


def run():
    ship_to_dc = NetworkFulfillmentModel.objects.get_or_create(
        name="Ship To DC", definition=""
    )
    drop_ship = NetworkFulfillmentModel.objects.get_or_create(
        name="Drop Ship", definition=""
    )

    grocery_vertical = NetworkVertical.objects.get_or_create(
        name="Grocery", definition=""
    )

    general_note = RequirementType.objects.get_or_create(name="GENERAL_NOTE")

    retailer = NetworkMemberProfileType.objects.get_or_create(name="RETAILER")
    three_pl = NetworkMemberProfileType.objects.get_or_create(name="3PL")

    member = Member.objects.get_or_create(organizationId="123")
    member_retailer = MemberProfile.objects.get_or_create(
        profileType=retailer[0], member=member[0]
    )
    member_3_pl = MemberProfile.objects.get_or_create(
        profileType=three_pl[0], member=member[0]
    )
