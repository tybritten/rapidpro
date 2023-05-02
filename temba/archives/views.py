from gettext import gettext as _

from smartmin.views import SmartCRUDL, SmartListView, SmartReadView

from django.http import HttpResponseRedirect
from django.urls import reverse

from temba.orgs.views import OrgObjPermsMixin, OrgPermsMixin
from temba.utils.views import ContentMenuMixin, SpaMixin

from .models import Archive


class ArchiveCRUDL(SmartCRUDL):
    model = Archive
    actions = ("read", "run", "message")
    permissions = True

    class BaseList(SpaMixin, OrgPermsMixin, ContentMenuMixin, SmartListView):
        title = _("Archive")
        fields = ("url", "start_date", "period", "record_count", "size")
        default_order = ("-start_date", "-period", "archive_type")
        paginate_by = 250

        def build_content_menu(self, menu):
            if not self.is_spa():
                archive_type = self.get_archive_type()
                for choice in Archive.TYPE_CHOICES:
                    if archive_type != choice[0]:
                        menu.add_link(f"{choice[1]} {_('Archives')}", reverse(f"archives.archive_{choice[0]}"))

        def get_queryset(self, **kwargs):
            queryset = super().get_queryset(**kwargs)

            # filter by our archive type
            return queryset.filter(org=self.org, archive_type=self.get_archive_type()).exclude(rollup_id__isnull=False)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["archive_types"] = Archive.TYPE_CHOICES
            context["selected"] = self.get_archive_type()
            return context

    class Run(BaseList):
        menu_path = "/settings/archives/run"

        @classmethod
        def derive_url_pattern(cls, path, action):
            return r"^%s/%s/$" % (path, Archive.TYPE_FLOWRUN)

        def derive_title(self):
            return _("Run Archives")

        def get_archive_type(self):
            return Archive.TYPE_FLOWRUN

    class Message(BaseList):
        menu_path = "/settings/archives/message"

        @classmethod
        def derive_url_pattern(cls, path, action):
            return r"^%s/%s/$" % (path, Archive.TYPE_MSG)

        def derive_title(self):
            return _("Message Archives")

        def get_archive_type(self):
            return Archive.TYPE_MSG

    class Read(OrgObjPermsMixin, SmartReadView):
        def render_to_response(self, context, **response_kwargs):
            return HttpResponseRedirect(self.get_object().get_download_link())
