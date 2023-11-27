#!/usr/bin/env python3

import argparse
import logging
import os.path
import sys
from pathlib import Path

import requests
from autopilot_tools.logger import logger
from autopilot_tools.vehicle import Vehicle
from autopilot_tools.enums import Devices
from autopilot_tools.px4.px_uploader import px_uploader

AUTOPILOT_TOOLS_DIR = Path(os.path.realpath(__file__)).parent.parent
DOWNLOAD_DIR = 'downloads'

#
# Serial port defaults.
#
# The uploader should be smarter than this. (c)
#

SERIAL_PORTS = {
    'darwin': "/dev/tty.usbmodemPX*,/dev/tty.usbmodem*",

    'linux': "/dev/serial/by-id/*_PX4_*,/dev/serial/by-id/usb-3D_Robotics*,"
             "/dev/serial/by-id/usb-The_Autopilot*,/dev/serial/by-id/usb-Bitcraze*,"
             "/dev/serial/by-id/pci-Bitcraze*,/dev/serial/by-id/usb-Gumstix*,"
             "/dev/serial/by-id/usb-UVify*,/dev/serial/by-id/usb-ArduPilot*,"
             "/dev/serial/by-id/ARK*,",

    'cygwin': "/dev/ttyS*",

    'win32': "COM32,COM31,COM30,COM29,COM28,COM27,COM26,COM25,COM24,COM23,COM22,"
             "COM21,COM20,COM19,COM18,COM17,COM16,COM15,COM14,COM13,COM12,COM11,"
             "COM10,COM9,COM8,COM7,COM6,COM5,COM4,COM3,COM2,COM1,COM0"

}[sys.platform]


def run_configurator():
    parser = argparse.ArgumentParser(
        prog='autopilot configurator',
        description='This utility flashes the MCU with the new firmware '
                    'and then uploads the new set of parameters from yaml file')

    parser.add_argument(
        '--firmware', default=None,
        help='path/link to the firmware file', type=str)
    parser.add_argument(
        '--config', dest='config', default=None, type=str,
        nargs='+', metavar='FW', help='Upload those set(s) of parameters to the MCU')
    parser.add_argument(
        '-d', '--device', dest='device', choices=Devices, type=str, default='serial',
        help='either udp (SITL) or serial (HITL)')
    parser.add_argument('-f', '--force-calibrate', dest='force_calibrate',
                        help='set this flag to force calibration', action='store_true')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')

    args = parser.parse_args()

    if args.config is None and args.firmware is None:
        parser.error('Nothing to do! Please provide either --firmware or --config')

    if args.verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.CRITICAL)
    configs = [os.path.abspath(config) for config in args.config] \
        if args.config is not None else None

    if args.device == Devices.serial and args.firmware is not None:
        if os.path.exists(args.firmware):
            path = os.path.abspath(args.firmware)
        elif requests.head(args.firmware, allow_redirects=True,
                           timeout=10).status_code == requests.codes.ok:  # pylint: disable=E1101
            logger.info(f'Link provided {args.firmware}. Attempting download')
            os.chdir(os.path.abspath(os.path.dirname(__file__)))
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            r = requests.get(args.firmware, timeout=300)
            filename = os.path.basename(args.firmware)
            path = os.path.join(DOWNLOAD_DIR, filename)
            with open(path, 'wb') as f:
                f.write(r.content)
            logger.info('Download successful')
        else:
            logger.critical(
                'Provided path is neither a local file nor a download link. Terminating')
            sys.exit(1)
        px_uploader([path], SERIAL_PORTS)

    if configs is not None or args.force_calibrate is not None:
        vehicle = Vehicle()
        vehicle.connect(args.device)

    if configs is not None:
        vehicle.reset_params_to_default()
        for conf in configs:
            vehicle.configure(conf, reboot=True)

    if args.force_calibrate is not None:
        logger.info('Forcing calibration')
        vehicle.force_calibrate()
        vehicle.reboot()


if __name__ == '__main__':
    run_configurator()
