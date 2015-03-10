#
# Python class file to manage archives
#
# Author: Kyle Manna < kmanna [at] fan [dot] tv >

import re
import os
import shutil
import logging
import tarfile
import subprocess

class ManifestArchive:
    def __init__(self, filename):
        self.filename = filename

        base = os.path.basename(self.filename)
        (root, ext) = os.path.splitext(base)
        self.ext = ext.lstrip('.')
        self.root = re.sub('\.tar.*$', '', root)

    def extract(self, dst='.', strip=True):
        # Leverage pxz if available
        if shutil.which('pxz') and self.ext == 'xz':
            logging.debug("Using pxz for compression")

            if strip: xform = '--strip 1'
            else: xform = ''

            # Hand it over to cmd line tools since multiple pipes in python is painful
            # and leverage pxz for best performance
            cmd_tar = 'pxz -d < {} | tar -xf - {}'.format(self.filename, xform)
            logging.debug("cmd: {}".format(cmd_tar))
            subprocess.call(cmd_tar, shell=True)


    def create(self, source, strip=True):
        # Leverage pxz if available
        if shutil.which('pxz') and self.ext == 'xz':
            logging.debug("Using pxz for compression")

            if strip:
                xform = '--xform \'s:^{}/:{}/:\''.format(source.lstrip('/'), self.root)
            else:
                xform = ''

            # Hand it over to cmd line tools since multiple pipes in python is painful
            # and leverage pxz for best performance
            cmd_tar = 'tar -cf - {} {} | pxz > {}'.format(source, xform, self.filename)
            logging.debug("cmd: {}".format(cmd_tar))
            subprocess.call(cmd_tar, shell=True)
        else:
            # Failsafe tarball + compression (slow!)
            with tarfile.open(self.filename, 'w:{}'.format(self.ext)) as tar:
                xform = None
                if strip:
                    xform = self.root
                tar.add(source, arcname=xform)

