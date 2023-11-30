# -*- coding: UTF-8 -*-
# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

# import time
import asyncio
import os
import threading
from channels.layers import get_channel_layer
# from django.utils import timezone
from django.core.management import BaseCommand, call_command
from django.conf import settings
from lino.modlib.linod.utils import CHANNEL_NAME
# , log_sock_path, worker_sock_path

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--force',
                            help="Force starts the runworker process even if a log_socket_file exists."
                                 " Use only in production server.",
                            action="store_true",
                            default=False
                            )
        # parser.add_argument("--skip-system-tasks",
        #                     help="Skips the system tasks coroutine",
        #                     action="store_true",
        #                     default=False)

    def handle(self, *args, **options):

        # if not settings.SITE.use_linod:
        #     logger.info("Run background jobs (system tasks)")
        #     # self.tasks = tasks = Tasks()
        #     # await database_sync_to_async(tasks.setup)()
        #     ar = settings.SITE.login()
        #     while True:
        #         next_dt = settings.SITE.models.linod.BackgroundTask.run_them_all(ar)
        #         if (to_sleep := (next_dt - timezone.now()).total_seconds()) > 0:
        #             # logger.info(f"next system tasks run: {next_dt}")
        #             time.sleep(to_sleep)
        #     return

        log_sock_path = settings.SITE.log_sock_path

        if log_sock_path and log_sock_path.exists() and not options.get('force'):
            raise Exception(
                f"log socket already exists: {log_sock_path}\n"
                "It's probable that a worker process is already running. "
                "Try: 'ps awx | grep linod' OR 'sudo supervisorctl status | grep worker'\n"
                "Or the last instance of the worker process did not finish properly. "
                "In that case remove the 'log_sock' file and run this command again.")

        # worker_sock_path.unlink(True)
        # log_sock_path.unlink(True)

        def start_channels():
            try:
                asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            call_command('runworker', CHANNEL_NAME)

        worker_thread = threading.Thread(target=start_channels)
        worker_thread.start()

        async def initiate_linod():
            layer = get_channel_layer()
            # if log_sock_path is not None:
            await layer.send(CHANNEL_NAME, {'type': 'log.server'})
            # await asyncio.sleep(1)
            await layer.send(CHANNEL_NAME, {'type': 'run.background.tasks'})

        loop = asyncio.get_event_loop()
        loop.run_until_complete(initiate_linod())

        try:
            worker_thread.join()
        except KeyboardInterrupt:
            print("Finishing thread...")
            worker_thread.join(0)
