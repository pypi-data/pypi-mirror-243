import logging
from collections import defaultdict
# import webbrowser
from datetime import datetime, timedelta
from enum import Enum
from ipaddress import IPv4Network, IPv6Network
from os import getcwd
from os.path import join
from time import sleep
from typing import Optional  # for type hinting
from typing import Any, Dict, List, Mapping, Sequence, Tuple, Union

from byteblower_test_framework.analysis import FrameLossAnalyser
from byteblower_test_framework.endpoint import Port  # for type hinting
from byteblower_test_framework.endpoint import IPv4Port, IPv6Port, NattedPort
from byteblower_test_framework.exceptions import log_api_error
from byteblower_test_framework.host import Server
from byteblower_test_framework.run import Scenario
from byteblower_test_framework.traffic import (FrameBlastingFlow, IPv4Frame,
                                               IPv6Frame)

from .definitions import (DEFAULT_FRAME_CONFIG, DEFAULT_TRIAL_DURATION,
                          INITIAL_BITRATE, LOGGING_PREFIX, MAX_ITERATIONS,
                          MAX_RETRY_COUNT, SLEEP_TIME, TEST_ACCURACY,
                          TOLERATED_FRAME_LOSS, TestProgress)
from .exceptions import (AllFramesLost, ConfigFileError, DiffSubnet,
                         DuplicateFrames, FrameSizeMissing, MaxRetriesReached,
                         OtherTrialException, PortLayer3Mismatch,
                         TrialException)
from .report_generator import html_report_generator, json_report_generator
from .scouting_flow import ScoutingFlow

__all__ = ('run', )

# Type aliases
_PortConfig = Mapping[str, Any]
_FlowConfig = Mapping[str, Any]


def run(test_config: dict, report_path: str, report_prefix: str) -> None:
    """RFC 2544 throughput test for a set of frame configurations.

    The frame configurations consist of frame size without CRC,
    expected bitrate, ...

    :param test_config: All configuration parameters for the RFC 2544
       throughput test
    :type test_config: dict
    :param report_path: Path where to store the report files
    :type report_path: str
    :param report_prefix: Prefix of the report files
    :type report_prefix: str
    :raises MaxRetriesReached: Occurs when number of trial retries exceeds
       the allowed :const:`MAX_RETRY_COUNT`
    """
    try:
        (
            frame_configs,
            max_iteration,
            duration,
            server_name,
            source_port_configs,
            destination_port_configs,
            test_progress,
        ) = _rfc2544_test_initialization(test_config)
        error_logs = defaultdict(list)
        rfc_test_results = {
            "configuration": {
                'server': server_name,
                'source': source_port_configs,
                'destination': destination_port_configs
            },
            "frame": [],
            "status": False,
            "error_logs": error_logs,
        }
        _rfc2544_all_frames(
            frame_configs,
            rfc_test_results,
            duration,
            max_iteration,
            test_progress,
        )

    except (ConfigFileError, KeyError) as error:
        logging.error("%s: %s", type(error).__name__, error)
    else:
        # Check if at least one result is recorded
        if rfc_test_results['frame']:
            logging.info("RFC 2544 throughput test has finished")
            rfc_test_results["status"] = not error_logs
            path_and_prefix = join(
                report_path or getcwd(),
                report_prefix + "_" + datetime.now().strftime('%Y%m%d_%H%M%S'))

            # Export results into  JSON file
            json_report_generator(rfc_test_results, path_and_prefix + ".json")

            # Gererate HTML report
            html_report_generator(
                rfc_test_results["configuration"],
                rfc_test_results["frame"],
                dict(error_logs),
                path_and_prefix + ".html",
                status=rfc_test_results["status"],
            )


def _rfc2544_all_frames(frame_configs, rfc_test_results, duration,
                        max_iteration, test_progress):
    error_logs = rfc_test_results['error_logs']
    server_name = rfc_test_results['configuration']['server']
    source_port_configs = rfc_test_results['configuration']['source']
    destination_port_configs = rfc_test_results['configuration']['destination']
    previous_max_bitrate = INITIAL_BITRATE
    last_index = len(frame_configs) - 1
    #overall_test_status: True  if all tests finished correctly, else is false
    overall_test_status = True
    for frame_conf_index, frame_conf in enumerate(frame_configs):
        try:
            frame_size = frame_conf['size']
            initial_bitrate = frame_conf.get("initial_bitrate",
                                             previous_max_bitrate)
            # Create new test scenario
            scenario = Scenario()
            # Connect to the ByteBlower Server
            server = Server(server_name)

            # initialize the ports
            source_port, destination_port = _initialize_ports(
                server, source_port_configs, destination_port_configs)
            # Initialize traffic flows
            udp_flow: FrameBlastingFlow
            udp_flow_analyzer: FrameLossAnalyser
            udp_flow, udp_flow_analyzer = _initialize_frameblasting_flows(
                scenario,
                source_port,
                destination_port,
                bitrate=initial_bitrate,
                frame_size=frame_size,
            )
            (
                test_bitrate,
                frame_test_duration,
                frame_results,
                frame_status,
            ) = _run_frame_trials(
                max_iteration,
                frame_conf,
                source_port,
                destination_port,
                scenario,
                duration,
                udp_flow_analyzer,
                test_progress,
                error_logs,
                initial_bitrate,
                udp_flow,
                frame_conf_index,
                last_index,
            )

            # Test duration for All trials of a frame size
            frame_results["test_duration"] = frame_test_duration
            previous_max_bitrate = test_bitrate
            rfc_test_results["frame"].append(frame_results)
            overall_test_status = overall_test_status and frame_status
        except OtherTrialException as error:
            overall_test_status = False
            frame_results["real_bitrate"] = error.test_bitrate
            # Test duration for all trials of a frame size
            frame_results["test_duration"] = error.frame_test_duration
            rfc_test_results["frame"].append(error.frame_results)
            _exception_handler(frame_size, error, error_logs)
        except Exception as error:
            overall_test_status = False
            _exception_handler(
                frame_size,
                error,
                error_logs,
                hint="Please check the configuration/setup for eventual errors",
            )
    rfc_test_results['status'] = overall_test_status


def _run_frame_trials(
    max_iteration,
    frame_conf,
    source_port,
    destination_port,
    scenario,
    duration,
    udp_flow_analyzer,
    test_progress: TestProgress,
    error_logs,
    initial_bitrate,
    udp_flow,
    frame_conf_index,
    last_index,
):
    # Limit number of iterations/framesize : 25 iteration/frame_size
    frame_size = frame_conf["size"]
    test_accuracy = frame_conf.get("accuracy", TEST_ACCURACY)
    test_bitrate = initial_bitrate
    tolerated_packet_loss = frame_conf.get("tolerated_frame_loss",
                                           TOLERATED_FRAME_LOSS)
    trials = []
    frame_results = {
        "size": frame_size,
        "tolerated_frame_loss": tolerated_packet_loss,
        "expected_bitrate": frame_conf["expected_bitrate"],
        "trials": trials,
        "real_bitrate": None,
        "test_duration": None,
    }
    max_bitrate = test_bitrate
    min_bitrate = 0
    restart_count = 0
    trial_count = 0
    frame_test_start = datetime.utcnow()
    frame_status = True
    try:
        # Limit number of iterations/framesize : 25 iteration/frame_size
        while True:
            if restart_count >= MAX_RETRY_COUNT:
                raise MaxRetriesReached(frame_size, MAX_RETRY_COUNT)
            try:

                # Initialize scouting flows
                _send_scouting_flows(source_port, destination_port)
                trial_duration, sent, received = _run_trial(
                    scenario,
                    duration,
                    udp_flow_analyzer,
                    frame_size,
                )
                test_progress.next_iteration()

            except TrialException as error:
                restart_count += 1
                _exception_handler(
                    frame_size,
                    error,
                    error_logs,
                    restart_count=restart_count,
                )
                continue
            except Exception as error:
                restart_count += 1
                _exception_handler(
                    frame_size,
                    error,
                    error_logs,
                    restart_count=restart_count,
                    hint=(
                        f"Unexpected exception occurred !!  Check ==> {error}"
                    ))
                continue
            # Save trial results
            test_status = (1 - (received / sent)) <= tolerated_packet_loss

            # trial_duration
            trials.append(
                _results_dict_generator(test_status, test_bitrate,
                                        received, sent, trial_duration,
                                        datetime.utcnow()))
            diff = (max_bitrate - min_bitrate) / 2
            if (test_status
                    and diff < test_accuracy) or trial_count > max_iteration:
                logging.info(
                    "Throughput test for frame size %d is done successfully",
                    frame_size)
                break
            else:
                # Calculate next biterate
                min_bitrate, max_bitrate, test_bitrate = _rfc2544_throughput(
                    test_status, test_bitrate, min_bitrate, max_bitrate, diff)
                # ! TODO: Move this functionality to the byteblower-test-framework
                # Update flow parameters
                frame_rate = test_bitrate / (frame_size * 8)
                udp_flow._frame_rate = frame_rate
                udp_flow._number_of_frames = int(frame_rate * duration)
                trial_count += 1
                # ! **************************************************************
            #! Maybe just Exception, since it should be the same behavior whatever the exception is
    except MaxRetriesReached as error:
        # Useful to avoid sleeping on last iteration
        if frame_conf_index == last_index:
            except_restart_count = None
        else:
            except_restart_count = restart_count
        frame_status = False
        _exception_handler(
            frame_size,
            error,
            error_logs,
            restart_count=except_restart_count,
        )

    except Exception as error:
        frame_test_duration = datetime.utcnow() - frame_test_start
        raise OtherTrialException(
            test_bitrate,
            frame_test_duration,
            frame_results,
        ) from error
    # Test duration for All trials of a frame size
    frame_test_duration = datetime.utcnow() - frame_test_start
    frame_results["real_bitrate"] = test_bitrate
    return test_bitrate, frame_test_duration, frame_results, frame_status


def _run_trial(
    scenario: Scenario,
    duration: int,
    udp_flow_analyzer,
    frame_size: int,
) -> Tuple[timedelta, int, int]:
    logging.info('%sStarting', LOGGING_PREFIX)
    scenario.run(maximum_run_time=timedelta(seconds=duration))
    trial_duration = scenario.duration
    # display progresss bar

    # ! TODO: Check when frame loss increases too much suddenly (Custom Exception)
    sent = udp_flow_analyzer.total_tx_packets
    received = udp_flow_analyzer.total_rx_packets
    if received == 0:
        raise AllFramesLost(frame_size)
    if received > sent:
        raise DuplicateFrames(frame_size, received - sent)
    return trial_duration, sent, received


def _rfc2544_throughput(test_status: bool, test_bitrate: float, min_bitrate,
                        max_bitrate, diff) -> Tuple[float, float, float]:
    if min_bitrate > max_bitrate:
        max_bitrate = min_bitrate
        min_bitrate = 0
    if diff == 0:  # min_bitrate == max_bitrate
        min_bitrate = 0.5 * min_bitrate
    if test_bitrate > max_bitrate:
        max_bitrate = test_bitrate
    diff = (max_bitrate - min_bitrate) / 2
    if not test_status:
        max_bitrate = test_bitrate
        test_bitrate -= diff
        min_bitrate = test_bitrate
    else:
        if min_bitrate == 0:
            test_bitrate += test_bitrate
        else:
            min_bitrate = test_bitrate
            test_bitrate += diff
        max_bitrate = test_bitrate

    return min_bitrate, max_bitrate, test_bitrate


def _rfc2544_test_initialization(test_config):
    frame_configs: List(Dict) = test_config.get('frame_configs',
                                                DEFAULT_FRAME_CONFIG)
    _frame_config_check(frame_configs)
    max_iteration = test_config.get('max_iterations', MAX_ITERATIONS)
    # Read server/ports configuration
    server_name = test_config['server']
    source_port_configs = test_config['source']
    destination_port_configs = test_config['destination']
    _port_config_check(source_port_configs)
    _port_config_check(destination_port_configs)
    # Trial duration
    duration = test_config.get('maximum_run_time', DEFAULT_TRIAL_DURATION)
    # Approximately 19 iteration / frame size => To be used only for progress bar
    estimated_test_iterations = len(frame_configs) * 19
    test_progress = TestProgress(estimated_test_iterations)
    return (
        frame_configs,
        max_iteration,
        duration,
        server_name,
        source_port_configs,
        destination_port_configs,
        test_progress,
    )


def _error_dict_generator(exception: str,
                          error_msg: str,
                          timestamp: str,
                          hint: Optional[str] = None) -> dict:

    results_dict = {
        "exception": exception,
        "error_msg": error_msg,
        "timestamp": timestamp,
    }
    if hint:
        results_dict["hint"] = hint
    return results_dict


def _exception_handler(
    frame_size: int,
    execption: Exception,
    error_logs,
    restart_count: Optional[int] = None,
    hint: Optional[str] = None,
) -> None:
    if hint:
        logging.exception(hint)
    else:
        logging.error("%s: %s", type(execption).__name__, execption)
    error_logs[frame_size].append(
        _error_dict_generator(
            type(execption).__name__, execption, datetime.utcnow(), hint))
    if restart_count is not None:
        logging.info("Attempt to restart test (%d) in %ds", restart_count,
                     SLEEP_TIME)
        sleep(SLEEP_TIME)


def _frame_config_check(frame_configs) -> None:
    for config in frame_configs:
        if config.get('size') is None:
            raise FrameSizeMissing()


def _port_config_check(port_config: dict) -> bool:
    # ! TODO: REQUIRED to move this test to the byteblower-test-framework / For Destination & Source
    if 'netmask' in port_config and 'gateway' in port_config:
        if 'ipv4' in port_config:
            if IPv4Network(
                    f"{port_config['ipv4']}/{port_config['netmask']}",
                    strict=False) != IPv4Network(
                        f"{port_config['gateway']}/{port_config['netmask']}",
                        strict=False):
                raise DiffSubnet()
        if 'ipv6' in port_config:
            if IPv6Network(
                    f"{port_config['ipv6']}/{port_config['netmask']}",
                    strict=False) != IPv6Network(
                        f"{port_config['gateway']}/{port_config['netmask']}",
                        strict=False):
                raise DiffSubnet()
    return True


def _results_dict_generator(status: bool, tested_Th: float, rx_packets: int,
                            tx_packets: int, duration: float,
                            timestamp: str) -> dict:

    results_dict = {
        "bitrate": tested_Th,
        "passed": status,
        "tx_packets": tx_packets,
        "rx_packets": rx_packets,
        "timestamp": timestamp,
        "duration": duration
    }
    return results_dict


class PortFactory:

    @staticmethod
    def build_port(server: Server, **port_config) -> Port:
        if 'ipv4' in port_config:
            nat = port_config.pop('nat', False)
            if nat:
                port_class = NattedPort
            else:
                port_class = IPv4Port
        elif 'ipv6' in port_config:
            port_class = IPv6Port
        name = port_config.pop('name', None)
        port = port_class(server, name=name, **port_config)
        return port


def _initialize_ports(
    server, source_port_configs: Union[Sequence[_PortConfig], _PortConfig],
    destination_port_configs: Union[Sequence[_PortConfig], _PortConfig]
) -> Tuple[Port, Port]:

    # Build source port
    logging.info('%sInitializing Source port', LOGGING_PREFIX)
    source_port: Port = PortFactory.build_port(server, **source_port_configs)
    logging.info(
        '%sInitialized Source port %r'
        ' with IP address %r, network %r', LOGGING_PREFIX, source_port.name,
        source_port.ip, source_port.network)

    # Build destination port
    destination_port: Port = PortFactory.build_port(server,
                                                    **destination_port_configs)
    logging.info(
        '%sInitialized Destination port %r'
        ' with IP address %r, network %r', LOGGING_PREFIX,
        destination_port.name, destination_port.ip, destination_port.network)

    return source_port, destination_port


def _send_scouting_flows(
    source_port: Port,
    destination_port: Port,
    udp_flow_config: Optional[_FlowConfig] = None,
    frame_size: Optional[int] = None,
) -> None:
    # UDP (Frame Blasting) flows
    if udp_flow_config is not None:
        _frameblasting_scouting_flows(source_port,
                                      destination_port,
                                      frame_size=frame_size)


class FlowType(Enum):
    ipv4 = 'IPv4'
    ipv6 = 'IPv6'


def _frameblasting_scouting_flows(source_port: Port,
                                  destination_port: Port,
                                  frame_size: Optional[int] = None) -> None:

    #! NOTE - **WORKAROUND** !
    #        * First sending upstream scouting frames to freshen NAT
    #        * entries avoiding unexpected traffic loss in either
    #        * direction, likely caused by *new NAT entries*.
    if isinstance(destination_port, NattedPort):
        _send_udp_scounting_flow(destination_port, source_port, frame_size)
    else:
        _send_udp_scounting_flow(source_port, destination_port, frame_size)


def _send_udp_scounting_flow(cpe_port: Port, nsi_port: Port,
                             frame_size: int) -> None:
    try:
        # First, send "upstream" traffic
        ScoutingFlow.run_udp_flow(cpe_port,
                                  nsi_port,
                                  frame_config={"length": frame_size})
        # Secondly, send "downstream" traffic
        ScoutingFlow.run_udp_flow(nsi_port,
                                  cpe_port,
                                  frame_config={"length": frame_size})
    except PortLayer3Mismatch as error:
        logging.warning("%s: Skipping upstream/downstream scouting flow",
                        error)


class FlowFactory:

    @staticmethod
    def create_udp_flow(
            source: Port,
            destination: Port,
            bitrate: float,
            frame_size: Optional[int] = None,
            flow_name_suffix: str = 'UDP traffic') -> FrameBlastingFlow:
        # Parse arguments
        # NOTE - Create a copy before altering.
        # Determine flow type and create frame
        if isinstance(source, IPv4Port):
            # Using default configuration if no frame_config given:
            frame = IPv4Frame(length=frame_size)
            flow_type = FlowType.ipv4
        elif isinstance(source, IPv6Port):
            # Using default configuration if no frame_config given:
            frame = IPv6Frame(length=frame_size)
            flow_type = FlowType.ipv6
        else:
            raise ValueError(
                f'Unsupported Port type: {type(source).__name__!r}')

        # Configure frame blasting flow
        destination_port = destination
        flow_name = '{} - {} {}'.format(destination_port.name, flow_type.value,
                                        flow_name_suffix)
        try:
            flow = FrameBlastingFlow(source,
                                     destination,
                                     name=flow_name,
                                     bitrate=bitrate,
                                     frame_list=[frame])
            return flow
        except Exception as error:
            logging.error(error)


@log_api_error
def _initialize_frameblasting_flows(
        scenario: Scenario,
        source_port: Port,
        destination_port: Port,
        bitrate: float,
        frame_size: int = None) -> Tuple[FrameBlastingFlow, FrameLossAnalyser]:
    # Create frame blasting flow & Add analyzer
    udp_flow = FlowFactory.create_udp_flow(source_port,
                                           destination_port,
                                           bitrate,
                                           frame_size=frame_size)
    udp_flow_analyser = FrameLossAnalyser()
    udp_flow.add_analyser(udp_flow_analyser)
    # Add frame blasting flow to the scenario
    scenario.add_flow(udp_flow)
    return udp_flow, udp_flow_analyser
