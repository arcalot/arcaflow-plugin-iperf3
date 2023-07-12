#!/usr/bin/env python3

from time import sleep
import unittest
import iperf3_plugin
import iperf3_schema
from multiprocessing.pool import ThreadPool
from arcaflow_plugin_sdk import plugin


def run_iperf3_server():
    server_input = iperf3_schema.ServerAllParams(
        run_duration=10,
        port=50000,
        interval=1,
        forceflush=True,
    )
    return iperf3_plugin.iperf3_server(server_input)


class iperf3Test(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            iperf3_plugin.ClientInputParams(
                host="foo",
                port=50000,
                interval=10,
                udp=True,
                bytes=100,
                bitrate=100000,
                format=iperf3_schema.Format.g,
            )
        )

        plugin.test_object_serialization(
            iperf3_plugin.ServerSuccessOutput(
                message="message",
            )
        )

        plugin.test_object_serialization(
            iperf3_plugin.ClientErrorOutput(error="This is an error")
        )

    def test_functional(self):
        pool = ThreadPool(processes=1)

        iperf3_server = pool.apply_async(run_iperf3_server)

        client_input = iperf3_schema.ClientInputParams(
            port=50000,
            interval=10,
            time=5,
        )

        sleep(2)

        client_output_id, client_output_data = iperf3_plugin.iperf3_client(client_input)

        self.assertEqual("success", client_output_id)
        self.assertEqual(
            "TCP", client_output_data.output.start["test_start"]["protocol"]
        )

        server_output_id, server_output_data = iperf3_server.get()

        self.assertEqual("success", server_output_id)
        self.assertEqual("message", server_output_data.message)


if __name__ == "__main__":
    unittest.main()
