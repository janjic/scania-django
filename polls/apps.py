from django.apps import AppConfig
from material.frontend.apps import ModuleMixin
from django.utils.translation import ugettext_lazy as _


class PollsConfig(ModuleMixin, AppConfig):
    name = 'polls'
    icon = '<i class="material-icons">extension</i>'
    verbose_name = _("Scania")

    def has_perm(self, user):
        return user.is_superuser
