#!/usr/bin/env python3

import json
import sys
import typing
import subprocess

from arcaflow_plugin_sdk import plugin
from iperf3_schema import (
    ServerAllParams,
    ServerSuccessOutput,
    ServerErrorOutput,
    ClientInputParams,
    ClientSuccessOutput,
    ClientErrorOutput,
    server_input_params_schema,
)


@plugin.step(
    id="server",
    name="iperf3 Server",
    description=(
        "Runs the passive iperf3 server to allow benchmarks between the client"
        " and this server"
    ),
    outputs={"success": ServerSuccessOutput, "error": ServerErrorOutput},
)
def iperf3_server(
    params: ServerAllParams,
) -> typing.Tuple[str, typing.Union[ServerSuccessOutput, ServerErrorOutput]]:
    
    # Set the iperf3 server command
    server_cmd = ["iperf3", "-s"]
    input_params = server_input_params_schema.serialize(params)
    for param, value in input_params.items():
        if type(value) == bool and not value:
            continue
        else:
            server_cmd.append(f"--{param}")
            if type(value) != bool:
                server_cmd.append(f"{value}")

    print(f"==>> Running the iperf server with a timeout of {params.run_duration} seconds")        
        
    # Start the passive server
    try:
        result = subprocess.run(
            server_cmd,
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
        return "success", ServerSuccessOutput("message")


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                # List your step functions here:
                iperf3_server,
            )
        )
    )
