#!/usr/bin/python3
#
# Will print a list of file names in a duplicity target_url
# duplicity is python3 (on ubuntu 18.04.1) and this script uses it's modules
# Note that backends make much use of environmental variables
#
#
# example usage:
#    pip3 install PyDrive
#    GOOGLE_DRIVE_SETTINGS=pydrive-settings.yaml ./duplicity_target_ls.py \
#                           "gdocs://example@gmail.com/duplicity"
#
# !! WARNING !!
# So far only tested on gdocs:// backend with these issues
# Depending on backend, target_url may be created if not already existing
# Also, gank output if a folder exists in target_url as folder has no size attibute
#
# Notes:
# GDrive backup failing with
#   Attempt 1 failed. RedirectMissingLocation: Redirected but the response is missing a Location: header
#   see:   https://github.com/googleapis/google-api-python-client/issues/803
#   fix:   pip3 install -U httplib2==0.15.0

import sys
from duplicity import log
from duplicity import config
from duplicity import backend

def duplicity_ls(target_url):
    try:
        backend.import_backends()
        be = backend.get_backend(target_url)
        filenames = be.list()

        config.backend_retry_delay = 1
        infos = be.query_info(filenames)

        for name,info in sorted(infos.items(), key=lambda x: x[0]):
            size = info['size']
            print("%s\t%d" % (name, size))

        return 0

    except Exception as e:
        print(str(e))
        return 1

if __name__== "__main__":
    try:
        log.setup()
        log.setverbosity(log.WARNING)
    except Exception as e:
        print("ERROR: Unable to setup duplicity log")
        print(str(e))
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage: %s target_url" % (sys.argv[0]))
        sys.exit(1)

    sys.exit( duplicity_ls(sys.argv[1]) )

