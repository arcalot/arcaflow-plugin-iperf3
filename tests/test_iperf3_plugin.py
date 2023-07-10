#!/usr/bin/env python3
import unittest
from arcaflow_plugin_iperf3 import iperf3_plugin
from arcaflow_plugin_sdk import plugin


class HelloWorldTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(iperf3_plugin.InputParams("John Doe"))

        plugin.test_object_serialization(iperf3_plugin.SuccessOutput("Hello, world!"))

        plugin.test_object_serialization(
            iperf3_plugin.ErrorOutput(error="This is an error")
        )

    def test_functional(self):
        input = iperf3_plugin.InputParams(name="Example Joe")

        output_id, output_data = iperf3_plugin.hello_world(input)

        # The example plugin always returns an error:
        self.assertEqual("success", output_id)
        self.assertEqual(
            output_data, iperf3_plugin.SuccessOutput("Hello, Example Joe!")
        )


if __name__ == "__main__":
    unittest.main()
