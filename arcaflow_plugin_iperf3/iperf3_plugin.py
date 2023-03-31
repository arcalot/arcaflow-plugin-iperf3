#!/usr/bin/env python3

import sys
import typing
import subprocess

from arcaflow_plugin_sdk import plugin
from iperf3_schema import (
    ServerInputParams,
    ServerSuccessOutput,
    ServerErrorOutput,
    ClientInputParams,
    ClientSuccessOutput,
    ClientErrorOutput,
)


@plugin.step(
    id="iperf3-server",
    name="iperf3 Server",
    description=(
        "Runs the passive iperf3 server to allow benchmarks between the client"
        " and this server"
    ),
    outputs={"success": ServerSuccessOutput, "error": ServerErrorOutput},
)
def iperf3_server(
    params: ServerInputParams,
) -> typing.Tuple[str, typing.Union[ServerSuccessOutput, ServerErrorOutput]]:
    # Start the passive server
    try:
        result = subprocess.run(
            ["iperf3", "-s"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=params.run_duration
        )
        # It should not end itself, so getting here means there was an
        # error.
        return "error", ServerErrorOutput(
            result.returncode,
            result.stdout.decode("utf-8") + result.stderr.decode("utf-8"),
        )
    except subprocess.TimeoutExpired:
        # Worked as intended. It doesn't end itself, so it finished when it
        # timed out.
        return "success", ServerSuccessOutput()


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                # List your step functions here:
                iperf3_server,
            )
        )
    )
