from __future__ import annotations

import queue
import threading
import time
import logging

import paho.mqtt.client as mq


class MQTTSerial:
    """A wrapper to make an MQTT topic pair look like a pyserial Serial object."""

    def __init__(self, host: str, tx_topic: str, rx_topic: str, timeout: float = 0.1):
        self._q = queue.Queue()
        self._cli = mq.Client()
        def _on_connect(c, _u, _f, rc):
            if rc == 0:
                logging.info(f"MQTTSerial connected to broker {host}")
                c.subscribe(rx_topic)
                logging.info(f"Subscribed to {rx_topic}")
            else:
                logging.error(f"MQTTSerial failed to connect, rc={rc}")
        self._cli.on_connect = _on_connect
        self._cli.on_message = lambda _c, _u, msg: self._q.put(msg.payload)
        self._cli.connect(host)
        self._cli.loop_start()
        self._tx_topic = tx_topic
        self.timeout = timeout

    def write(self, data) -> int:  # type: ignore[override]
        """Publish *raw bytes* to the transmit topic.

        The Feetech SDK sometimes hands us a *list* of ints or a ``bytearray``.
        Normalise everything to ``bytes`` so that the paho-mqtt client accepts
        the payload without raising ``TypeError``.
        """
        if isinstance(data, list):
            data = bytes(data)
        elif isinstance(data, bytearray):
            data = bytes(data)
        # Safety: make sure we only send bytes hereafter.
        if not isinstance(data, (bytes, str)):
            raise TypeError(f"Unsupported payload type for MQTTSerial.write: {type(data)}")
        logging.info(f"MQTTSerial TX → {self._tx_topic}: {data.hex() if isinstance(data, bytes) else data}")
        self._cli.publish(self._tx_topic, data, qos=0)
        return len(data)

    def read(self, n: int = 1) -> bytes:
        """Read up to n bytes from the receive topic queue."""
        buf = bytearray()
        deadline = time.time() + self.timeout
        while len(buf) < n and time.time() < deadline:
            try:
                # Read all available bytes from the queue up to n
                chunk = self._q.get_nowait()
                logging.info(f"MQTTSerial RX ← {self._tx_topic}: {chunk.hex()}")
                buf.extend(chunk)
            except queue.Empty:
                time.sleep(0.001)
        return bytes(buf)

    def flush(self):
        """No-op for MQTT."""
        pass

    @property
    def in_waiting(self) -> int:
        """Return the number of bytes in the receive queue."""
        # This is an approximation as one queue item may have multiple bytes
        return self._q.qsize()

    def close(self):
        """Disconnect the MQTT client."""
        self._cli.loop_stop()
        self._cli.disconnect()
