from urllib.parse import urlparse

from django.conf import settings
from django.contrib import admin
from django.contrib.redirects.admin import RedirectAdmin
from django.contrib.redirects.models import Redirect

from import_export.admin import ImportMixin
from import_export.fields import Field
from import_export.resources import ModelResource

admin.site.unregister(Redirect)


def ensure_trailing_slash(string):
    return string + "/" if not string.endswith('/') else string


def check_leading_slash(string):
    return "/" + string if not string.startswith("/") else string


def extract_path(string):
    """Extract path from full url with encasing slashes"""
    parsed = urlparse(string)
    path = parsed.path if parsed.netloc else string

    path_with_trailing_slash = ensure_trailing_slash(path)
    return check_leading_slash(path_with_trailing_slash)


def check_full_url(url):
    """
    If url checks scheme is available otherwise checks
    for encasing slashes
    """

    scheme = "https://"
    url = ensure_trailing_slash(url)
    if not url.startswith(scheme) and "." in url.split("/", 1)[0]:
        return scheme + url

    if "." not in url:
        return check_leading_slash(url)

    return url


class RedirectResource(ModelResource):

    class Meta:
        model = Redirect
        fields = (
            "old_path",
            "new_path",
            "site_id",
        )
        import_id_fields = ()

    def before_import_row(self, row, row_number=None, **kwargs):
        row["old_path"] = extract_path(row["old_path"])
        row["new_path"] = check_full_url(row["new_path"])
        row["site_id"] = settings.SITE_ID

        return row

    def skip_row(self, instance, original, row, import_validation_errors):
        """
        Overwritten method from Resource class
        https://django-import-export.readthedocs.io/en/latest/api_resources.html?highlight=skip_row#import_export.resources.Resource.skip_row
        """
        # second part of condition deals with bug that reads empty rows
        # https://github.com/django-import-export/django-import-export/issues/1192#1281
        old_path = row["old_path"]
        new_path = row["new_path"]

        is_redirect_not_unique = bool(Redirect.objects.filter(old_path=old_path))
        skip = is_redirect_not_unique or (not old_path) or (not new_path)

        return skip

    def before_save_instance(self, instance, using_transactions, dry_run):
        instance.site_id = settings.SITE_ID

        return instance


@admin.register(Redirect)
class RedirectAdminExtension(ImportMixin, RedirectAdmin):
    """
    Extension of the base RedirectAdmin in order to add
    a custom "import redirects" form
    """

    resource_class = RedirectResource
