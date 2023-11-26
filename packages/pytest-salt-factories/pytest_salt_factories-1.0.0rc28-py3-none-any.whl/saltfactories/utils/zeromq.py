"""
A ZeroMQ socket monitor.
"""
import logging
import pprint
import time
from typing import Any
from typing import Dict

import zmq
from zmq.utils.monitor import recv_monitor_message

log = logging.getLogger(__name__)


def event_monitor_thread_target(monitor_name: str, monitor: zmq.Socket) -> None:
    """
    A thread that logs events.

    monitor: a zmq monitor socket, from calling:  my_zmq_socket.get_monitor_socket()
    """
    if zmq.zmq_version_info() < (4, 0):
        raise RuntimeError("monitoring in libzmq version < 4.0 is not supported")

    log.debug("ZMQMonitor(%s) starting...", monitor_name)
    event_map = {}
    for name in dir(zmq):
        if name.startswith("EVENT_"):
            value = getattr(zmq, name)
            event_map[value] = name

    log.info("ZMQMonitor(%s) Events:\n%s", monitor_name, pprint.pformat(event_map))

    while True:
        try:
            while monitor.poll():
                evt: Dict[str, Any] = {}
                mon_evt = recv_monitor_message(monitor)
                evt.update(mon_evt)
                evt["description"] = event_map[evt["event"]]
                log.warning("ZMQMonitor(%s) event:\n%s", monitor_name, pprint.pformat(evt))
                if evt["event"] == zmq.EVENT_MONITOR_STOPPED:
                    break
        except zmq.error.ContextTerminated:
            break
        except RuntimeError as exc:
            log.exception("ZMQMonitor(%s) exception: %s", monitor_name, exc)
            time.sleep(1)

    monitor.close()
    log.debug("ZMQMonitor(%s) stopped...")
