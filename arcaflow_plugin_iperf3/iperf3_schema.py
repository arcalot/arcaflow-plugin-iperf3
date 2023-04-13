#!/usr/bin/env python3

import enum
import re
import typing
from dataclasses import dataclass
from arcaflow_plugin_sdk import schema, plugin


class Format(enum.Enum):
    k = "k"
    m = "m"
    g = "g"
    t = "t"
    K = "K"
    M = "M"
    G = "G"
    T = "T"


class Protocol(enum.Enum):
    TCP = "TCP"
    UDP = "UDP"
    SCTP = "SCTP"


class Congestion(enum.Enum):
    # TODO Confirm this is fully inclusive
    reno = "reno"
    cubic = "cubic"
    bic = "bic"
    htcp = "htcp"
    vegas = "vegas"
    westwood = "westwood"
    YeAH = "YeAH"


unit_bits = schema.Units(
    schema.Unit("b", "b", "bit", "bits"),
    {
        1024: schema.Unit("K", "K", "kibibit", "kibibits"),
        1048576: schema.Unit("M", "M", "mibibit", "mibibits"),
        1073741824: schema.Unit("G", "G", "gibibit", "gibibits"),
        1099511627776: schema.Unit("T", "T", "tebibit", "tebibits"),
    },
)

unit_bytes = schema.Units(
    schema.Unit("B", "B", "byte", "bytes"),
    {
        1024: schema.Unit("K", "K", "kibibyte", "kibibytes"),
        1048576: schema.Unit("M", "M", "mibibyte", "mibibytes"),
        1073741824: schema.Unit("G", "G", "gibibyte", "gibibytes"),
        1099511627776: schema.Unit("T", "T", "tebibyte", "tebibytes"),
    },
)

kmgt_description = (
    "- accepts [KMGT] suffixes to indicate kibi-, mibi-, -gibi, or tebi-"
    "(2^10); integer input implies base unit (bits or bytes)"
)

unit_miliseconds = schema.Units(
    schema.Unit("ms", "ms", "milisecond", "miliseconds"),
    {
        1000: schema.Unit("s", "s", "second", "seconds"),
        60000: schema.Unit("m", "m", "minute", "minutes"),
    },
)

unit_seconds = schema.Units(
    schema.Unit("s", "s", "second", "seconds"),
    {
        60: schema.Unit("m", "m", "minute", "minutes"),
    },
)


@dataclass
class CommonInputParams:
    port: typing.Annotated[
        typing.Optional[int],
        schema.name("port"),
        schema.description("server port to listen on/connect to"),
    ] = None
    format: typing.Annotated[
        typing.Optional[Format],
        schema.name("format"),
        schema.description(
            "[kmgtKMGT] format to report: kibi-, mibi, gibi, tebi- bits/Bytes"
        ),
    ] = None
    interval: typing.Annotated[
        typing.Optional[int],
        schema.name("interval"),
        schema.description("seconds between periodic throughput reports"),
    ] = None
    affinity: typing.Annotated[
        typing.Optional[str],
        schema.name("affinity"),
        schema.pattern(re.compile(r"^\d+$|^\d+,\d+$")),
        schema.description("[n/n,m] set CPU affinity"),
    ] = None
    bind: typing.Annotated[
        typing.Optional[str],
        schema.name("bind"),
        schema.description("bind to the interface associated with the address <host>"),
    ] = None
    forceflush: typing.Annotated[
        typing.Optional[bool],
        schema.name("force flush"),
        schema.description("force flushing output at every interval"),
    ] = False

    # Params from the iperf3 input not used in the input schema
    # file name: typing.Annotated[
    #     schema.name(""),
    #     schema.description("xmit/recv the specified file"),
    # ]
    # verbose: typing.Annotated[
    #     schema.name(""),
    #     schema.description("more detailed output"),
    # ]
    # json: typing.Annotated[
    #     schema.name(""),
    #     schema.description("output in JSON format"),
    # ]
    # logfile: typing.Annotated[
    #     schema.name(""),
    #     schema.description("f               send output to a log file"),
    # ]
    # debug: typing.Annotated[
    #     schema.name(""),
    #     schema.description("emit debugging output"),
    # ]
    # version: typing.Annotated[
    #     schema.name(""),
    #     schema.description("show version information and quit"),
    # ]
    # help: typing.Annotated[
    #     schema.name(""),
    #     schema.description("show this message and quit"),
    # ]


@dataclass
class ServerInputParams(CommonInputParams):
    {}

    # TODO - Implement rsa and private key credentials handling

    # Params from the iperf3 input not used in the input schema
    # Server specific:
    #   -s, --server              run in server mode
    #   -D, --daemon              run the server as a daemon
    #   -I, --pidfile file        write PID file
    #   -1, --one-off             handle one client connection then exit
    #   --rsa-private-key-path    path to the RSA private key used to decrypt
    #                             authentication credentials
    #   --authorized-users-path   path to the configuration file containing user


#                             credentials

server_input_params_schema = plugin.build_object_schema(ServerInputParams)


@dataclass
class ServerAllParams(ServerInputParams):
    # TODO replace this once signaling is available
    run_duration: typing.Annotated[
        typing.Optional[int],
        schema.name("server run duration"),
        schema.description("time in seconds to run the iperf3 server before exiting"),
    ] = 600


@dataclass
class ClientInputParams(CommonInputParams):
    host: typing.Annotated[
        typing.Optional[str],
        schema.name("server host"),
        schema.description(
            "the hostname or IP address of the iperf3 server; defaults to localhost"
        ),
    ] = "localhost"
    udp: typing.Annotated[
        typing.Optional[bool],
        schema.name("use UDP protocol"),
        schema.conflicts("sctp"),
        schema.required_if("udp_counters_64bit"),
        schema.description("use the UDP protocol for network traffic"),
    ] = None
    sctp: typing.Annotated[
        typing.Optional[bool],
        schema.name("use SCTP protocol"),
        schema.conflicts("udp"),
        schema.required_if("xbind"),
        schema.required_if("nstreams"),
        schema.description("use the SCTP protocol for network traffic"),
    ] = None
    xbind: typing.Annotated[
        typing.Optional[bool],
        schema.name("sctp xbind"),
        schema.description("bind SCTP association to links"),
    ] = None
    nstreams: typing.Annotated[
        typing.Optional[int],
        schema.name("sctp nstreams"),
        schema.description("number of SCTP streams"),
    ] = None
    connect_timeout: typing.Annotated[
        typing.Optional[int],
        schema.id("connect-timeout"),
        schema.name("connect timeout"),
        schema.description("timeout for control connection setup (ms)"),
    ] = None
    bitrate: typing.Annotated[
        typing.Optional[int],
        schema.name("bitrate"),
        schema.units(unit_bits),
        schema.description(
            "target bitrate in bits/sec (0 for unlimited)"
            "(default 1 Mbit/sec for UDP, unlimited for TCP) (optional slash "
            f"and packet count for burst mode) {kmgt_description}"
        ),
    ] = None
    pacing_timer: typing.Annotated[
        typing.Optional[int],
        schema.id("pacing-timer"),
        schema.name("pacing timer"),
        schema.units(unit_miliseconds),
        schema.description("set the timing for pacing, in microseconds (default 1000)"),
    ] = None
    fq_rate: typing.Annotated[
        typing.Optional[int],
        schema.id("fq-rate"),
        schema.name("fair-queuing rate"),
        schema.units(unit_bits),
        schema.description(
            "enable fair-queuing based socket pacing inbits/sec (Linux only) "
            f"{kmgt_description}"
        ),
    ] = None
    time: typing.Annotated[
        typing.Optional[int],
        schema.name("time"),
        schema.units(unit_seconds),
        schema.conflicts("bytes"),
        schema.conflicts("blockcount"),
        schema.description("time in seconds to transmit for (default 10 secs)"),
    ] = None
    bytes: typing.Annotated[
        typing.Optional[int],
        schema.name("bytes"),
        schema.units(unit_bytes),
        schema.conflicts("time"),
        schema.conflicts("blockcount"),
        schema.description(f"number of bytes to transmit {kmgt_description}"),
    ] = None
    blockcount: typing.Annotated[
        typing.Optional[int],
        schema.name("block count"),
        schema.units(unit_bytes),
        schema.conflicts("time"),
        schema.conflicts("bytes"),
        schema.description(
            f"number of blocks (packets) to transmit {kmgt_description}"
        ),
    ] = None
    length: typing.Annotated[
        typing.Optional[int],
        schema.name("length"),
        schema.units(unit_bytes),
        schema.description(
            "length of buffer to read or write (default 128 KB for TCP, "
            f"dynamic or 1460 for UDP) {kmgt_description}"
        ),
    ] = None
    cport: typing.Annotated[
        typing.Optional[int],
        schema.name("client port"),
        schema.description(
            "bind to a specific client port (TCP and UDP, default: ephemeral port)"
        ),
    ] = None
    parallel: typing.Annotated[
        typing.Optional[int],
        schema.name("parallel"),
        schema.description("number of parallel client streams to run"),
    ] = None
    reverse: typing.Annotated[
        typing.Optional[bool],
        schema.name("reverse"),
        schema.description("run in reverse mode (server sends, client receives)"),
    ] = False
    window: typing.Annotated[
        typing.Optional[int],
        schema.name("window size"),
        schema.units(unit_bytes),
        schema.description(f"set window size / socket buffer size {kmgt_description}"),
    ] = None
    congestion: typing.Annotated[
        typing.Optional[Congestion],
        schema.name("congestion algorithm"),
        schema.description(
            "set TCP congestion control algorithm (Linux and FreeBSD only)"
        ),
    ] = None
    set_mss: typing.Annotated[
        typing.Optional[int],
        schema.id("set-mss"),
        schema.name("maximum segment size"),
        schema.units(unit_bytes),
        schema.description(
            f"set TCP/SCTP maximum segment size (MTU - 40 bytes) {kmgt_description}"
        ),
    ] = None
    no_delay: typing.Annotated[
        typing.Optional[bool],
        schema.id("no-delay"),
        schema.name("TCP/SCTP no delay"),
        schema.description("set TCP/SCTP no delay, disabling Nagle's Algorithm"),
    ] = False
    version4: typing.Annotated[
        typing.Optional[bool],
        schema.name("IPv4 only"),
        schema.conflicts("version6"),
        schema.description("only use IPv4"),
    ] = False
    version6: typing.Annotated[
        typing.Optional[bool],
        schema.name("IPv6 only"),
        schema.conflicts("version4"),
        schema.description("only use IPv6"),
    ] = False
    tos: typing.Annotated[
        typing.Optional[int],
        # TODO support octal and hex values?
        schema.name("IP type of service"),
        schema.min(0),
        schema.max(255),
        schema.description("set the IP type of service, 0-255."),
    ] = None
    dscp: typing.Annotated[
        typing.Optional[int],
        # TODO support octal and hex values (and "symbolic"?)?
        schema.name("dscp"),
        schema.min(0),
        schema.max(63),
        schema.description("set the IP dscp value, 0-63"),
    ] = None
    flowlabel: typing.Annotated[
        typing.Optional[int],
        schema.name(""),
        schema.description("set the IPv6 flow label (only supported on Linux)"),
    ] = None
    zerocopy: typing.Annotated[
        typing.Optional[bool],
        schema.name("zero copy"),
        schema.description("use a 'zero copy' method of sending data"),
    ] = False
    omit: typing.Annotated[
        typing.Optional[int],
        schema.name("omit first N seconds"),
        schema.description("omit the first n seconds"),
    ] = None
    title: typing.Annotated[
        typing.Optional[str],
        # TODO validate length maximum (what is it?)
        schema.name("output prefix"),
        schema.description("prefix every output line with this string"),
    ] = None
    get_server_output: typing.Annotated[
        typing.Optional[bool],
        schema.id("get-server-output"),
        schema.name("get server output"),
        schema.description("get results from server"),
    ] = False
    udp_counters_64bit: typing.Annotated[
        typing.Optional[bool],
        # TODO only use with UDP
        schema.id("udp-counters-64bit"),
        schema.name("UDP 64-bit counters"),
        schema.description("use 64-bit counters in UDP test packets"),
    ] = None

    # TODO implement rsa public key

    # Params from the iperf3 input not used in the input schema
    # Client specific:
    #   --username                username for authentication
    #   --rsa-public-key-path     path to the RSA public key used to encrypt
    #                             authentication credentials
    #   -c, --client    <host>    run in client mode, connecting to <host>
    # sctp: typing.Annotated[
    #     schema.name(""),
    #     schema.description("                    use SCTP rather than TCP"),
    # ] = None
    # udp: typing.Annotated[
    #     schema.name(""),
    #     schema.description("                 use UDP rather than TCP"),
    # ] = None

    # [KMG] indicates options that support a K/M/G suffix for kilo-, mega-, or giga-


client_input_params_schema = plugin.build_object_schema(ClientInputParams)


@dataclass
class ClientOutputCategories:
    start: typing.Dict[str, typing.Any]
    intervals: typing.List[typing.Any]
    end: typing.Dict[str, typing.Any]


client_output_categories_schema = plugin.build_object_schema(ClientOutputCategories)


@dataclass
class ClientSuccessOutput:
    output: ClientOutputCategories


@dataclass
class ServerSuccessOutput:
    message: str


@dataclass
class ServerErrorOutput:
    error: str


@dataclass
class ClientErrorOutput:
    error: str
