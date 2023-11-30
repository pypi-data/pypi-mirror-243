# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import rt, dd

from .choicelists import PublishingStates
from .mixins import Publishable


# @dd.receiver(dd.pre_analyze)
# def inject_previous_page_fields(sender, **kw):
#     print("20231103", PublisherViews.get_list_items())
#     for pv in PublisherViews.get_list_items():
#         print("20231103", pv)
#         dd.inject_field(
#             pv.table_class.model, 'previous_page',
#             dd.ForeignKey("self", null=True, blank=True,
#                 verbose_name=_("Previous page")))



# @dd.schedule_daily()
# def update_publisher_pages(ar):
#     # BaseRequest(parent=ar).run(settings.SITE.site_config.check_all_summaries)
#     # rt.login().run(settings.SITE.site_config.check_all_summaries)
#     for pv in PublisherViews.get_list_items():
#     # for m in rt.models_by_base(Published, toplevel_only=True):
#         prev = None
#         count = 0
#         ar.logger.info("Update published pages for %s ...", pv)
#         for obj in pv.get_publisher_pages():
#             obj.set_previous_page(prev)
#             prev = obj
#             count += 1
#         ar.logger.info("%d pages for %s have been updated.", count, pv)
