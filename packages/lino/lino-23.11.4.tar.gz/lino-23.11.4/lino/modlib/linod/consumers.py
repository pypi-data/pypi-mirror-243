# -*- coding: UTF-8 -*-
# Copyright 2022-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import atexit
import asyncio
import json
import os
import pickle
import signal
import socket
import logging
import struct
import sys
from pathlib import Path

try:
    from pywebpush import webpush, WebPushException
except ImportError:
    webpush = None

from asgiref.sync import sync_to_async
from django.conf import settings
from django.utils import timezone
from channels.db import database_sync_to_async
from channels.consumer import AsyncConsumer

# from lino.modlib.linod.tasks import Tasks
from lino.utils.socks import send_through_socket, get_from_socket

from lino import logger

# used for debugging, when no 'log' dir exists
# if not logger.handlers:
#     logger.addHandler(logging.StreamHandler())
#     logger.setLevel(logging.INFO)


class LogReceiver(asyncio.Protocol):

    # def connection_made(self, transport):
    #     print("20231019 connection_made", transport)

    def data_received(self, data: bytes):
        data = pickle.loads(data[4:]) # first four bytes gives the size of the rest of the data
        record = logging.makeLogRecord(data)
        # print("20231019 data_received", record)
        # 20231019 server_logger.handle(record)
        logger.handle(record)

# from .utils import log_sock_path, worker_sock_path

class LinodConsumer(AsyncConsumer):

    # tasks: Tasks
    clients = set()

    async def log_server(self, event=None):
        asyncio.ensure_future(self._log_server())

    async def _log_server(self):
        # 'log.server' in linod.py
        log_sock_path = settings.SITE.log_sock_path
        if log_sock_path is None:
            logger.info("No log server because there is no log directory.")
            return
        logger.info("Start the log server...")
        atexit.register(self.remove_sock_file)
        loop = asyncio.get_running_loop()
        # log_sock_path.unlink(True)
        self.remove_sock_file()
        server = await loop.create_unix_server(LogReceiver, log_sock_path)
        # await server.serve_forever()
        try:
            async with server:
                await server.serve_forever()
        finally:
            self.remove_sock_file()

    def remove_sock_file(self):
        settings.SITE.log_sock_path.unlink(missing_ok=True)
        # worker_sock_path.unlink(True)

    async def run_background_tasks(self, event: dict):
        # 'run.background.jobs' in `pm linod`
        asyncio.ensure_future(self._run_background_tasks())

    async def _run_background_tasks(self):
        logger.info("Start the background tasks runner using %s...", logger)
        BackgroundTask = settings.SITE.models.linod.BackgroundTask
        # self.tasks = tasks = Tasks()
        # await database_sync_to_async(tasks.setup)()
        ar = settings.SITE.login()
        while True:
            # asyncio.ensure_future
            next_dt = await BackgroundTask.run_them_all(ar)
            # next_dt = await database_sync_to_async(tasks.run)()
            # if not next_dt:
            #     break
            # if next_dt is True:
            #     continue
            if (to_sleep := (next_dt - timezone.now()).total_seconds()) <= 0:
                continue
            logger.debug(f"Let background jobs sleep for {to_sleep} seconds.")
            await asyncio.sleep(to_sleep)

    async def send_push(self, event):
        # 'send.push' in notify.send_notification()
        # logger.info("Push to %s : %s", user or "everyone", data)
        data = event['data']
        user = event['user_id']
        if user is not None:
            user = settings.SITE.models.users.User.objects.get(pk=user)
        kwargs = dict(
            data=json.dumps(data),
            vapid_private_key=settings.SITE.plugins.notify.vapid_private_key,
            vapid_claims={
                'sub': "mailto:{}".format(settings.SITE.plugins.notify.vapid_admin_email)
            }
        )
        if user is None:
            subs = settings.SITE.models.notify.Subscription.objects.all()
        else:
            subs = settings.SITE.models.notify.Subscription.objects.filter(user=user)
        for sub in subs:
            sub_info = {
                'endpoint': sub.endpoint,
                'keys': {
                    'p256dh': sub.p256dh,
                    'auth': sub.auth,
                },
            }
            try:
                req = webpush(subscription_info=sub_info, **kwargs)
            except WebPushException as e:
                if e.response.status_code == 410:
                    sub.delete()
                else:
                    raise e

    # async def dev_worker(self, event: dict):
    #     # dev.worker in linod
    #     # worker_sock = str(worker_sock_path)
    #
    #     def add_client(sock: socket.socket) -> None:
    #         self.clients.add(get_from_socket(sock))
    #         sock.close()
    #
    #     def remove_client(sock: socket.socket, close: bool = True) -> None:
    #         self.clients.discard(get_from_socket(sock))
    #         if close:
    #             sock.close()
    #
    #     def client_exists(sock: socket.socket) -> None:
    #         if get_from_socket(sock) in self.clients:
    #             send_through_socket(sock, b'true')
    #         else:
    #             send_through_socket(sock, b'false')
    #         handle_msg(sock)
    #
    #     def process_remove_get(sock: socket.socket) -> None:
    #         remove_client(sock, False)
    #         data = pickle.dumps({'clients': len(self.clients), 'pid': os.getpid()})
    #         send_through_socket(sock, data)
    #         sock.close()
    #
    #     SIGNALS = {
    #         b'add': add_client,
    #         b'exists': client_exists,
    #         b'remove': remove_client,
    #         b'remove_get': process_remove_get,
    #         b'close': lambda sock: sock.close()
    #     }
    #
    #     def handle_msg(client_sock: socket.socket) -> None:
    #         msg = get_from_socket(client_sock)
    #         if msg not in SIGNALS:
    #             send_through_socket(client_sock, b"Invalid signal!")
    #             client_sock.close()
    #         else:
    #             SIGNALS[msg](client_sock)
    #
    #     try:
    #         with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    #             worker_sock_path.unlink(True)
    #             sock.bind(str(worker_sock_path))
    #             sock.listen(5)
    #             while True:
    #                 client_sock, _ = sock.accept()
    #                 handle_msg(client_sock)
    #     finally:
    #         worker_sock_path.unlink(True)

    # async def job_list(self, event):
    #     async def do():
    #         with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    #             sockd = str(settings.SITE.site_dir / 'sockd')
    #             sock.connect(sockd)
    #             jobs = await database_sync_to_async(self.tasks.status)()
    #             data = pickle.dumps(jobs)
    #             await asyncio.sleep(1)
    #             send_through_socket(sock, data)
    #     asyncio.ensure_future(do())
