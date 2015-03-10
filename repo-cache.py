#!/usr/bin/env python3
#
# Author: Kyle Manna <kyle [at] kylemana [dot] com >
#
# Example invocation:
# ./manifest-cache.py -u https://android.googlesource.com/platform/manifest -b android-1.6_r1

import os
import sys
import glob
import json
import logging
import tarfile
import subprocess
import xml.etree.ElementTree as ET
#import archives.ManifestArchive as archive
from archives import ManifestArchive
import http.client
import argparse
from time import gmtime, strftime

if __name__ == '__main__':

    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--manifest-branch", help="manifest branch or revision")
    parser.add_argument("-u", "--manifest-url", help="manifest repository location")
    parser.add_argument("-j", "--jobs", help="projects to fetch simultaneously")
    parser.add_argument("-i", "--input", help="tarball input")
    parser.add_argument("-o", "--output", help="tarball output")

    args = parser.parse_args()

    name = args.manifest_branch
    origdir = os.getcwd()

    base = name

    if args.input:
        archive = ManifestArchive(args.input)
        archive.extract('.')

    # Build repo command
    cmd = ['repo', 'init']

    if args.manifest_branch:
        cmd.extend(['--manifest-branch', args.manifest_branch])

    if args.manifest_url:
        cmd.extend(['--manifest-url', args.manifest_url])

    # Run repo init
    logging.info("Running: {}".format(str(cmd)))
    ret = subprocess.call(cmd)

    # Run repo sync
    cmd_sync = ['repo', 'sync']

    if args.jobs:
        cmd_sync.extend(['--jobs', args.jobs])

    logging.info("Running: {}".format(str(cmd_sync)))
    ret = subprocess.call(cmd_sync)

    if args.output:
        logging.info("Creating tarball @ {}".format(args.output))
        archive = ManifestArchive(args.output)
        archive.create('.')

