from django.conf.urls import include
from django.urls import re_path
from django.utils.translation import gettext_lazy as _

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail import hooks
from wagtail.admin.menu import Menu, SubmenuMenuItem

from wagtaildonate import admin_urls
from wagtaildonate.settings import donate_settings


def register_admin_urls():
    return [re_path(r"^donate/", include(admin_urls, namespace="wagtaildonate_admin"))]


class PaymentsMenu(SubmenuMenuItem):
    def is_shown(self, request):
        payment_perms = [
            "wagtaildonate.can_export_donations",
            "wagtaildonate.can_export_recurring_donations",
            "wagtaildonate.can_export_pay_ins",
        ]
        return any(request.user.has_perm(perm) for perm in payment_perms)


def register_payments_menu():
    kwargs = (
        {"classname": "icon icon-cogs"}
        if WAGTAIL_VERSION >= (5, 2)
        else {"classnames": "icon icon-cogs"}
    )
    return PaymentsMenu(
        _("Payments"), Menu(register_hook_name="register_payments_menu_item"), **kwargs
    )


def register_general_wagtail_hooks():
    if donate_settings.DONATION_EXPORT_ENABLED:
        hooks.register("register_admin_urls", register_admin_urls)
        hooks.register("register_admin_menu_item", register_payments_menu)
