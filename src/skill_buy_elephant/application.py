import logging
from typing import Dict

import fastapi
import prometheus_client as prom  # type: ignore
from pythonjsonlogger import jsonlogger  # type: ignore
from starlette_exporter import PrometheusMiddleware  # type: ignore
from starlette_exporter import handle_metrics

from .graphite_client import graphite_client
from .skill import skill


def json_logging_prepare():
    logging.basicConfig(level=logging.DEBUG)
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.handlers = [log_handler]


json_logging_prepare()


req_summary_time = prom.Summary(
    'skill_time', 'Time spent processing a request'
)
req_counter = prom.Counter('skill_counter', 'Skill requests counter')


app = fastapi.FastAPI()
app.add_middleware(PrometheusMiddleware)
app.add_middleware(
    PrometheusMiddleware,
    app_name=graphite_client.graphite_prefix, group_paths=True
)
app.add_route("/metrics", handle_metrics)


@app.post("/")
@req_summary_time.time()
def main(body: Dict) -> Dict:
    logging.info('Request: %r', body)

    req_counter.inc(1)

    try:
        graphite_client.handle_request('query')

        response: Dict = dict()
        skill.handle_dialog(body, response)

        logging.info('Response: %r', response)
    except Exception as ex:
        logging.exception(
            'Exception catched: %r', ex
        )
        graphite_client.handle_error()

    return response


@app.get("/")
@req_summary_time.time()
def get_main() -> Dict:
    req_counter.inc(1)
    graphite_client.handle_request('query_get')
    return {
        "status": "OK",
        "tag": "4",
    }


@app.get("/readiness_probe")
def get_readiness_probe() -> Dict:
    return healthz()


@app.get("/liveness_probe")
def get_liveness_probe() -> Dict:
    return healthz()


@app.get("/startup_probe")
def get_startup_probe() -> Dict:
    return healthz()


def healthz() -> Dict:
    return {
        "status": "OK"
    }
