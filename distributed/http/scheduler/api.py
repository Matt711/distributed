from __future__ import annotations

import json

from distributed.http.utils import RequestHandler


class APIHandler(RequestHandler):
    def get(self):
        self.write("API V1")
        self.set_header("Content-Type", "text/plain")


class RetireWorkersHandler(RequestHandler):
    async def post(self):
        self.set_header("Content-Type", "text/json")
        scheduler = self.server
        try:
            params = json.loads(self.request.body)
            workers_info = await scheduler.retire_workers(**params)
            self.write(json.dumps(workers_info))
        except Exception as e:
            self.set_status(400, str(e))
            self.write(json.dumps({"Error": "Bad request"}))


class WorkersToCloseHandler(RequestHandler):
    async def post(self):
        self.set_header("Content-Type", "text/json")
        scheduler = self.server
        try:
            params = json.loads(self.request.body)
            workers_to_close = {"workers": scheduler.workers_to_close(**params)}
            self.write(json.dumps(workers_to_close))
        except Exception as e:
            self.set_status(400, str(e))
            print(str(e))
            self.write(json.dumps({"Error": "Bad request"}))


class GetWorkersHandler(RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/json")
        scheduler = self.server
        response = {
            "num_workers": len(scheduler.workers),
            "workers": [
                {"name": ws.name, "address": ws.address}
                for ws in scheduler.workers.values()
            ],
        }
        self.write(json.dumps(response))


class AdaptiveTargetHandler(RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/json")
        scheduler = self.server
        desired_workers = scheduler.adaptive_target()
        response = {
            "workers": desired_workers,
        }
        self.write(json.dumps(response))


routes: list[tuple] = [
    ("/api/v1", APIHandler, {}),
    ("/api/v1/retire_workers", RetireWorkersHandler, {}),
    ("/api/v1/workers_to_close", WorkersToCloseHandler, {}),
    ("/api/v1/get_workers", GetWorkersHandler, {}),
    ("/api/v1/adaptive_target", AdaptiveTargetHandler, {}),
]
