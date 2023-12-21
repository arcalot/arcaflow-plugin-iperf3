import sys
from arcaflow_plugin_sdk import plugin as plugin_sdk
import arcaflow_plugin_iperf3.iperf3_plugin as iperf3_plugin

def main():    
    sys.exit(
        plugin_sdk.run(
            plugin_sdk.build_schema(
                iperf3_plugin.iperf3_server,
                iperf3_plugin.iperf3_client,
            )
        )
    )


if __name__ == "__main__":
    main()