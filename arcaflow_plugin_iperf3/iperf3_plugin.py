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
    client_input_params_schema,
    client_output_categories_schema,
)


def run_iperf3(mode, input_params):
    # Set the iperf3 command
    # iperf3_cmd = ["iperf3", f"--{mode}", "--verbose", "--json", "--debug"]
    iperf3_cmd = ["iperf3", "--json"]

    for param, value in input_params.items():
        if param == "protocol":
            if value == "TCP":
                continue
            elif value == "UDP":
                iperf3_cmd.append("--udp")
            elif value == "SCTP":
                iperf3_cmd.append("--sctp")
        elif param == "host":
            iperf3_cmd.append("--client")
            iperf3_cmd.append(f"{value}")
        elif type(value) is bool and not value:
            continue
        else:
            iperf3_cmd.append(f"--{param}")
            if type(value) is not bool:
                iperf3_cmd.append(f"{value}")

    if mode == "server":
        print()
        # TODO Refactor to run both client and server from function
    else:
        return subprocess.Popen(
            iperf3_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
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
    server_cmd = ["iperf3", "--server", "--json"]
    input_params = server_input_params_schema.serialize(params)
    for param, value in input_params.items():
        if type(value) is bool and not value:
            continue
        else:
            server_cmd.append(f"--{param}")
            if type(value) is not bool:
                server_cmd.append(f"{value}")

    print(
        f"==>> Running the iperf server with a timeout of {params.run_duration} seconds"
    )

    # Start the passive server
    try:
        result = subprocess.run(
            server_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=params.run_duration,
        )
        # It should not end itself, so getting here means there was an
        # error.
        return "error", ServerErrorOutput(
            "error ({}):\nstdout:\n{}\nstderr:\n{}".format(
                result.returncode,
                result.stdout.decode("utf-8"),
                result.stderr.decode("utf-8"),
            )
        )
    except subprocess.TimeoutExpired:
        # Worked as intended. It doesn't end itself, so it finished when it
        # timed out.
        return "success", ServerSuccessOutput("message")


@plugin.step(
    id="client",
    name="iperf3 Client",
    description="Runs the iperf3 client workload",
    outputs={"success": ClientSuccessOutput, "error": ClientErrorOutput},
)
def iperf3_client(
    params: ClientInputParams,
) -> typing.Tuple[str, typing.Union[ClientSuccessOutput, ClientErrorOutput]]:
    input_params = client_input_params_schema.serialize(params)

    with run_iperf3("client", input_params) as master_process:
        outs, errs = master_process.communicate()

    if errs is not None and len(errs) > 0 and b"Broken pipe" not in errs:
        return "error", ClientErrorOutput(
            "error:\nstdout:\n{}\nstderr:\n{}".format(
                outs.decode("utf-8"),
                errs.decode("utf-8"),
            )
        )
    if b"error" in outs:
        return "error", ClientErrorOutput(
            "Errors found in run. Output:\n" + outs.decode("utf-8")
        )

    json_out = json.loads(outs.decode("utf-8"))

    # Debug output
    print(json_out)

    output = client_output_categories_schema.unserialize(json_out)

    return "success", ClientSuccessOutput(output)


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                iperf3_server,
                iperf3_client,
            )
        )
    )
