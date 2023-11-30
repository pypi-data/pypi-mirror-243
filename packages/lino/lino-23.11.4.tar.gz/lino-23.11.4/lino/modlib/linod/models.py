# -*- coding: UTF-8 -*-
# Copyright 2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# See https://dev.lino-framework.org/plugins/linod.html

import logging
import sys
import traceback
from datetime import timedelta
from io import StringIO
from django.conf import settings
from django.utils import timezone
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

from lino.api import dd, rt, _
from lino.core.roles import SiteStaff
from lino import logger
from lino.mixins import Sequenced
from lino.modlib.checkdata.choicelists import Checker
from lino.modlib.system.mixins import RecurrenceSet
from .choicelists import Procedures, LogLevels


class RunNow(dd.Action):
    label = _("Run now")
    select_rows = True
    # icon_name = 'bell'
    # icon_name = 'lightning'

    def run_from_ui(self, ar, **kwargs):
        # print("20231102 RunNow", ar.selected_rows)
        for obj in ar.selected_rows:
            assert isinstance(obj, rt.models.linod.BackgroundTask)
            if True:
                # Just mark the task as to be executed asap by linod.
                obj.last_start_time = None
                obj.disabled = False
                obj.full_clean()
                obj.save()
            else:
                # Runs the task myself (not in background).
                async_to_sync(obj.start_task)(ar)
        ar.set_response(refresh=True)


class BackgroundTask(Sequenced, RecurrenceSet):
    class Meta:
        abstract = dd.is_abstract_model(__name__, 'BackgroundTask')
        app_label = 'linod'
        verbose_name = _("Background task")
        verbose_name_plural = _("Background tasks")

    procedure = Procedures.field(strict=False, unique=True)
    log_level = LogLevels.field(default='INFO')
    disabled = dd.BooleanField(_("Disabled"), default=False)
    last_start_time = dd.DateTimeField(_("Started at"), null=True, editable=False)
    last_end_time = dd.DateTimeField(_("Ended at"), null=True, editable=False)
    message = dd.RichTextField(_("Logged messages"), format='plain', editable=False)

    run_now = RunNow()

    def disabled_fields(self, ar):
        df = super().disabled_fields(ar)
        df.add('procedure')
        return df

    @classmethod
    async def run_them_all(cls, ar):
        # Loops once over all tasks and runs those that are due to run. Returns
        # the suggested time for a next loop.

        # ar.debug("20231013 run_them_all()")
        now = timezone.now()
        next_time = now + timedelta(seconds=12)
        tasks = cls.objects.filter(disabled=False)
        async for self in tasks:
            # ar.info("20231010 start %s", jr)
            if self.last_start_time is None:
                # print("20231021 1 gonna start", self)
                await self.start_task(ar)
                assert self.last_end_time is not None
                nst = self.get_next_suggested_date(ar, self.last_end_time)
                next_time = min(next_time, nst)
            elif self.last_end_time is None:
                run_duration = now - self.last_start_time
                if run_duration > timedelta(hours=2):
                    self.last_end_time = now
                    self.message = "Killed after running more than 2 hours"
                    self.full_clean()
                    self.save()
                    # self.disabled = True
                # print("20231021 skip running task", self)
                # pass
            else:
                nst = self.get_next_suggested_date(ar, self.last_end_time)
                if nst > now:
                    # print("20231021 not yet starting", self)
                    pass
                else:
                    # print("20231021 2 gonna start", self)
                    await self.start_task(ar)
                    assert self.last_end_time is not None
                    nst = self.get_next_suggested_date(ar, self.last_end_time)
                # else:
                #     ar.debug("20231013 Skip %s for now", self)
                next_time = min(next_time, nst)
        return next_time

    def is_running(self):
        return self.last_end_time is None and self.last_start_time is not None

    async def start_task(self, ar):
        # print("20231102 start_task", self)
        if self.is_running():
            raise Warning(_("{} is already running").format(self))
            # return
        self.last_start_time = timezone.now()
        # forget about any previous run:
        self.last_end_time = None
        self.message = ''
        # print("20231102 full_clean")
        await database_sync_to_async(self.full_clean)()
        # print("20231102 save")
        await database_sync_to_async(self.save)()
        with ar.capture_logger(self.log_level.num_value) as out:
            ar.info("Start %s...", self)
            # ar.info("Start %s using %s...", self, self.log_level)
            # print("20231021", ar.logger)
            try:
                await self.procedure.run(ar)
                # job.message = ar.response.get('info_message', '')
                self.message = out.getvalue()
            except Exception as e:
                self.message = out.getvalue()
                self.message += '\n' + ''.join(traceback.format_exception(e))
                self.disabled = True
        self.last_end_time = timezone.now()
        self.message = "<pre>" + self.message + "</pre>"
        await database_sync_to_async(self.full_clean)()
        await database_sync_to_async(self.save)()

    def __str__(self):
        r = "{} #{} {}".format(
            self._meta.verbose_name, self.pk, self.procedure.value)
        # if self.disabled:
        #     r += " ('disabled')"
        return r

    @dd.displayfield("Status")
    def status(self, ar=None):
        if self.is_running():
            return _("Running since {}").format(dd.ftl(self.last_start_time))
        if self.disabled:
            return _("Disabled")
        if self.last_start_time is None:
            return _("Not started")
        next_time = self.get_next_suggested_date(
            ar, self.last_end_time or timezone.now())
        if next_time is None:
            return _("Idle")
        return _("Scheduled to run at {}").format(dd.ftl(next_time))



# class Jobs(dd.Table):
#     model = 'linod.Job'
#     required_roles = dd.login_required(SiteStaff)
#     column_names = "start_time end_time rule message *"
#     detail_layout = """
#     rule
#     start_time end_time
#     message
#     """


# class JobsByRule(Jobs):
#     master_key = 'rule'
#     column_names = "start_time end_time message *"
#

class BackgroundTasks(dd.Table):
    # label = _("System tasks")
    model = 'linod.BackgroundTask'
    required_roles = dd.login_required(SiteStaff)
    column_names = "seqno procedure log_level disabled status *"
    detail_layout = """
    seqno procedure every every_unit
    log_level disabled status
    last_start_time last_end_time
    message
    """
    insert_layout = """
    procedure
    every every_unit
    """


class JobsChecker(Checker):
    """
    Checks for procedures that do not yet have a background task.
    """
    verbose_name = _("Check for missing background tasks")
    model = None

    def get_checkdata_problems(self, obj, fix=False):
        BackgroundTask = rt.models.linod.BackgroundTask

        for proc in Procedures.get_list_items():
            if BackgroundTask.objects.filter(procedure=proc).count() == 0:
                msg = _("No background task for {}").format(proc)
                yield (True, msg)
                if fix:
                    logger.debug("Create background task for %r", proc)
                    jr = BackgroundTask(procedure=proc, **proc.kwargs)
                        # every_unit=proc.every_unit, every=proc.every_value)
                    if jr.every_unit == "secondly":
                        jr.log_level = "WARNING"
                    jr.full_clean()
                    jr.save()

JobsChecker.activate()
