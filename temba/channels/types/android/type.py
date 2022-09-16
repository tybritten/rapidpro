from django.utils.translation import gettext_lazy as _

from temba.contacts.models import URN

from ...models import ChannelType
from .views import ClaimView, UpdateForm


class AndroidType(ChannelType):
    """
    An Android relayer app channel type
    """

    code = "A"
    category = ChannelType.Category.PHONE

    name = "Android"
    icon = "icon-channel-android"

    claim_blurb = _(
        "Works in any country and uses the cell phone plan you already have. You just need an Android phone to get started."
    )

    claim_view = ClaimView
    update_form = UpdateForm

    schemes = [URN.TEL_SCHEME]
    max_length = -1
    attachment_support = False
    free_sending = False
    show_config_page = False
