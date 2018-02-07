from __future__ import unicode_literals
from __future__ import absolute_import

from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard
from jet.utils import get_admin_site_name

class DefaultIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):

        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            children=[
                [_('Return to site'), '/admin'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ],
            column=0,
            order=0
        ))
        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('auth.*', 'djcelery.*', ),
            column=2,
            order=0
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('auth.*',),
            column=2,
            order=0
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            20,
            column=2,
            order=1
        ))
