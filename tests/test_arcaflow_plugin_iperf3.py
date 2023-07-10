#!/usr/bin/env python3
import unittest
import iperf3_plugin
from arcaflow_plugin_sdk import plugin


class HelloWorldTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            iperf3_plugin.ClientInputParams(
                host="foo",
                port=50000,
                interval=10,
                udp=True,
                bytes=100,
                # FIXME -- Apparent bug in test_object_serializtion not
                # accepting a string value when using units
                # bitrate='100K',
                # FIXME -- Apparent bug as above but with enums
                # format='g',
            )
        )

        # TODO -- Add output serialization test
        # plugin.test_object_serialization(
        #     iperf3_plugin.SuccessOutput(

        #     )
        # )

        plugin.test_object_serialization(
            iperf3_plugin.ClientErrorOutput(error="This is an error")
        )

    # TODO -- Add functional tests
    # def test_functional(self):
    #     input = iperf3_plugin.InputParams(name="Example Joe")

    #     output_id, output_data = iperf3_plugin.hello_world(input)

    #     # The example plugin always returns an error:
    #     self.assertEqual("success", output_id)
    #     self.assertEqual(
    #         output_data, iperf3_plugin.SuccessOutput("Hello, Example Joe!")
    #     )


if __name__ == "__main__":
    unittest.main()
