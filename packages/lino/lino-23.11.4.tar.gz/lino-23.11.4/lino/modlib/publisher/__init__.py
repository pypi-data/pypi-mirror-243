# -*- coding: UTF-8 -*-
# Copyright 2020-2022 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api.ad import Plugin

from lino.core.dashboard import DashboardItem


class PublisherDashboardItem(DashboardItem):

    def __init__(self, pv, **kwargs):
        self.publisher_view = pv
        super().__init__(str(pv), **kwargs)
        # print("20220927 dashboard item", pv.publisher_location)

    def render(self, ar, **kwargs):
        yield "<h3>{}</h3>".format(self.publisher_view.table_class.label)
        sar = self.publisher_view.table_class.request(parent=ar)
        for obj in sar:
            yield "<p>{}</p>".format(sar.row_as_paragraph(obj))


class Plugin(Plugin):

    needs_plugins = ["lino.modlib.jinja", "lino.modlib.bootstrap3"]

    locations = []

    # def on_ui_init(self, kernel):
    def post_site_startup(self, site):
        super().post_site_startup(site)
        from .renderer import Renderer
        self.renderer = Renderer(self)
        # ui.bs3_renderer = self.renderer

        from .mixins import Publishable
        locations = []
        for loc, view in self.locations:
            app_label, model_name = view.split(".")
            app = site.models.get(app_label)
            cls = getattr(app, model_name, None)
            # assert issubclass(cls, Table)
            if not issubclass(cls.model, Publishable):
                raise Exception(
                    "location {}: model is a {}, which is not Publishable".format(
                        view, type(cls.model)))

            cls.model._lino_publisher_location = loc
            locations.append((loc, cls))
        self.locations = tuple(locations)

    # ui_handle_attr_name = "publisher"

    def get_patterns(self):
        from django.urls import re_path as url
        from lino.core.utils import models_by_base
        from . import views
        # from .choicelists import PublisherViews
        # raise Exception("20220927")
        # print("20220927", list(PublisherViews.get_list_items()))

        # for pv in PublisherViews.get_list_items():
        for publisher_location, table_class in self.locations:
            # print("20220927", pv.publisher_location)
            # if publisher_location is not None:
            yield url('^{}/(?P<pk>.+)$'.format(publisher_location),
                views.Element.as_view(table_class=table_class))

        yield url('^$', views.Index.as_view())
        # yield url('^login$',views.Login.as_view())
