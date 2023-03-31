#!/usr/bin/env python3

import enum
import re
import typing
from dataclasses import dataclass
from arcaflow_plugin_sdk import schema


# # Usage: iperf3 [-s|-c host] [options]
# #        iperf3 [-h|--help] [-v|--version]

# # Server or Client:

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

# class Congestion(enum.Enum):


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
        schema.description("[kmgtKMGT] format to report: Kbits, Mbits, Gbits, Tbits"),
    ] = None
    interval: typing.Annotated[
        typing.Optional[int],
        schema.name("interval"),
        schema.description("seconds between periodic throughput reports"),
    ] = None
    # file name: typing.Annotated[
    #     schema.name(""),
    #     schema.description("xmit/recv the specified file"),
    # ]
    affinity: typing.Annotated[
        #FIXME How do I set the pattern expected?
        typing.Optional[re.Pattern],
        schema.name("affinity"),
        schema.description("n/n,m      set CPU affinity"),
    ] = None
    bind: typing.Annotated[
        typing.Optional[str],
        schema.name("bind"),
        schema.description("bind to the interface associated with the address <host>"),
    ] = None
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
    forceflush: typing.Annotated[
        typing.Optional[bool],
        schema.name("force flush"),
        schema.description("force flushing output at every interval"),
    ] = False
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
    #TODO replace this once signaling is available
    run_duration: typing.Annotated[
        int,
        schema.name("server run duration"),
        schema.description("Time in seconds to run the iperf3 server before exiting"),
    ]
    #TODO
# # Server specific:
# #   -s, --server              run in server mode
# #   -D, --daemon              run the server as a daemon
# #   -I, --pidfile file        write PID file
# #   -1, --one-off             handle one client connection then exit
# #   --rsa-private-key-path    path to the RSA private key used to decrypt
# #                             authentication credentials
# #   --authorized-users-path   path to the configuration file containing user
# #                             credentials

@dataclass
class ClientInputParams(CommonInputParams):
# # Client specific:
# #   -c, --client    <host>    run in client mode, connecting to <host>
    # sctp: typing.Annotated[
    #     schema.name(""),
    #     schema.description("                    use SCTP rather than TCP"),
    # ] = None
    protocol: typing.Annotated[
        typing.Optional[Protocol],
        schema.name("protocol"),
        schema.description("the protocol to use - TCP, UDP, or SCTP (default TCP)")
    ] = "TCP"
# #   -X, --xbind <name>        bind SCTP association to links
# #   --nstreams      #         number of SCTP streams
    # udp: typing.Annotated[
    #     schema.name(""),
    #     schema.description("                 use UDP rather than TCP"),
    # ] = None
    connect_timeout: typing.Annotated[
        typing.Optional[int],
        schema.id("connect-timeout"),
        schema.name("connect timeout"),
        schema.description("timeout for control connection setup (ms)"),
    ] = None
    bitrate: typing.Annotated[
        typing.Optional[int],
        #TODO implement units
        schema.name("bitrate"),
        schema.description(" #[KMG][/#]  target bitrate in bits/sec (0 for unlimited) (default 1 Mbit/sec for UDP, unlimited for TCP) (optional slash and packet count for burst mode)"),
    ] = None
    pacing_timer: typing.Annotated[
        typing.Optional[int],
        #TODO implement units
        schema.id("pacing-timer"),
        schema.name("pacing timer"),
        schema.description(" #[KMG]     set the timing for pacing, in microseconds (default 1000)"),
    ] = None
    fq_rate: typing.Annotated[
        typing.Optional[int],
        #TODO implement units
        schema.id("fq-rate"),
        schema.name("fair-queuing rate"),
        schema.description(" #[KMG]          enable fair-queuing based socket pacing inbits/sec (Linux only)"),
    ] = None                    
    time: typing.Annotated[
        typing.Optional[int],
        schema.name("time"),
        schema.description("      #         time in seconds to transmit for (default 10 secs)"),
    ] = None
    bytes: typing.Annotated[
        typing.Optional[int],
        #TODO implement units
        #TODO bytes and time inputs should be mutually exclusive
        schema.name("bytes"),
        schema.description("     #[KMG]    number of bytes to transmit (instead of -t)"),
    ] = None
    blockcount: typing.Annotated[
        typing.Optional[int],
        #TODO implement units
        schema.name("block count"),
        schema.description(" #[KMG]   number of blocks (packets) to transmit (instead of -t or -n)"),
    ] = None
    length: typing.Annotated[
        typing.Optional[int],
        #TODO implement units
        schema.name("length"),
        schema.description("    #[KMG]    length of buffer to read or write (default 128 KB for TCP, dynamic or 1460 for UDP)"),
    ] = None
    cport: typing.Annotated[
        typing.Optional[int],
        schema.name("client port"),
        schema.description("         <port>    bind to a specific client port (TCP and UDP, default: ephemeral port)"),
    ] = None
    parallel: typing.Annotated[
        typing.Optional[int],
        schema.name("parallel"),
        schema.description("  #         number of parallel client streams to run"),
    ] = None
    reverse: typing.Annotated[
        typing.Optional[bool],
        schema.name("reverse"),
        schema.description("             run in reverse mode (server sends, client receives)"),
    ] = False
    window: typing.Annotated[
        typing.Optional[int],
        #TODO implement units
        schema.name("window size"),
        schema.description("    #[KMG]    set window size / socket buffer size"),
    ] = None
    #TODO It's unclear what input iperf3 expects for this parameter
    # congestion: typing.Annotated[
    #     typing.Optional[Congestion],
    #     schema.name("congestion algorithm"),
    #     schema.description(" <algo>   set TCP congestion control algorithm (Linux and FreeBSD only)"),
    # ] = None
    set_mss: typing.Annotated[
        typing.Optional[int],
        #TODO implement units
        typing.id("set-mss"),
        schema.name("maximum segment size"),
        schema.description("   #         set TCP/SCTP maximum segment size (MTU - 40 bytes)"),
    ] = None
    no_delay: typing.Annotated[
        typing.Optional[bool],
        schema.id("no-delay"),
        schema.name("TCP/SCTP no delay"),
        schema.description("            set TCP/SCTP no delay, disabling Nagle's Algorithm"),
    ] = False
    version4: typing.Annotated[
        typing.Optional[bool],
        #TODO version4 and version6 should be mutually exclusive
        schema.name("IPv4 only"),
        schema.description("            only use IPv4"),
    ] = False
    version6: typing.Annotated[
        typing.Optional[bool],
        schema.name("IPv6 only"),
        schema.description("            only use IPv6"),
    ] = False
    tos: typing.Annotated[
        typing.Optional[int],
        #TODO validate range
        #TODO support octal and hex values
        schema.name("IP type of service"),
        schema.description(" N               set the IP type of service, 0-255.The usual prefixes for octal and hex can be used, i.e. 52, 064 and 0x34 all specify the same value."),
    ] = None
    dscp: typing.Annotated[
        typing.Optional[int],
        #TODO validate range
        #TODO support octal and hex values (and "symbolic"?)
        schema.name("dscp"),
        schema.description(" N or --dscp val    set the IP dscp value, either 0-63 or symbolic. Numeric values can be specified in decimal, octal and hex (see --tos above)."),
    ] = None
    flowlabel: typing.Annotated[
        typing.Optional[int],
        schema.name(""),
        schema.description(" N         set the IPv6 flow label (only supported on Linux)"),
    ] = None
    zerocopy: typing.Annotated[
        typing.Optional[bool],
        schema.name("zero copy"),
        schema.description("            use a 'zero copy' method of sending data"),
    ] = False
    omit: typing.Annotated[
        typing.Optional[int],
        schema.name("omit first N seconds"),
        schema.description(" N              omit the first n seconds"),
    ] = None
    title: typing.Annotated[
        typing.Optional[str],
        #TODO validate length maximum (what is it?)
        schema.name("output prefix"),
        schema.description(" str           prefix every output line with this string"),
    ] = None
    get_server_output: typing.Annotated[
        typing.Optional[bool],
        schema.id("get-server-output"),
        schema.name("get server output"),
        schema.description("       get results from server"),
    ] = False
    udp_counters_64bit: typing.Annotated[
        typing.Optional[bool],
        #TODO only use with UDP
        schema.id("udp-counters-64bit"),
        schema.name("UDP 64-bit counters"),
        schema.description("      use 64-bit counters in UDP test packets"),
    ] = None
    #TODO implement auth
# #   --username                username for authentication
# #   --rsa-public-key-path     path to the RSA public key used to encrypt
# #                             authentication credentials

# # [KMG] indicates options that support a K/M/G suffix for kilo-, mega-, or giga-

@dataclass
class ServerSuccessOutput:
    """
    This is the output data structure for the success case.
    """

    message: str


@dataclass
class ClientSuccessOutput:
    """
    This is the output data structure for the success case.
    """

    message: str


@dataclass
class ServerErrorOutput:
    """
    This is the output data structure in the error  case.
    """

    error: str


@dataclass
class ClientErrorOutput:
    """
    This is the output data structure in the error  case.
    """

    error: str