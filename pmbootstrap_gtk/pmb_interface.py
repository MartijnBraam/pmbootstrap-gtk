import sys
import logging
from pmb.helpers.devices import list as _list_devices


def args():
    import pmb.parse
    sys.argv = ["pmbootstrap.py", "chroot"]
    args = pmb.parse.arguments()
    args.log = args.work + "/log_testsuite.txt"
    pmb.helpers.logging.init(args)
    return args


def list_supported_devices():
    raw = _list_devices(args())
    return list(sorted(raw))
