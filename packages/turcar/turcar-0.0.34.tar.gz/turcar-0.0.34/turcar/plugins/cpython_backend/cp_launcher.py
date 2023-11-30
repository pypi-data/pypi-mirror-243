# -*- coding: utf-8 -*-

"""
This file is run by CPythonProxy

(Why separate file for launching? I want to have clean global scope
in toplevel __main__ module (because that's where user scripts run), but backend's global scope
is far from clean.
I could also do python -c "from backend import MainCPythonBackend: MainCPythonBackend().mainloop()",
but looks like this gives relative __file__-s on imported modules.)
"""
import ast

# NB! This module can be also imported (when querying its path for uploading)
if __name__ == "__main__":
    import ast
    import os.path
    import sys

    # make sure turcar folder is in sys.path during startup
    turcar_container = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    if turcar_container not in sys.path:
        # We're running with non-turcar interpreter or env
        sys.path.insert(0, turcar_container)
        using_temp_augmented_sys_path = True
    else:
        using_temp_augmented_sys_path = False

    if sys.platform == "darwin":
        try:
            os.getcwd()
        except Exception:
            print(
                "\nNB! Potential problems detected, see\nhttps://github.com/turcar/turcar/wiki/MacOSX#catalina\n",
                file=sys.stderr,
            )

    if not sys.version_info > (3, 8):
        print(
            "This version of turcar only supports Python 3.8 and later.\n"
            + "Choose another interpreter from Tools => Options => Interpreter",
            file=sys.stderr,
        )
        sys.exit(1)
    import turcar
    from turcar import report_time

    report_time("Before importing MainCPythonBackend")
    from turcar.common import PROCESS_ACK
    from turcar.plugins.cpython_backend.cp_back import MainCPythonBackend

    turcar.prepare_turcar_user_dir()
    turcar.configure_backend_logging()
    print(PROCESS_ACK)

    if using_temp_augmented_sys_path:
        # Don't make turcar container available for user programs.
        # NB! Need to do it before constructing the backend as it would clean the main scope and the flag would be gone.
        from logging import getLogger

        assert sys.path[0] == turcar_container
        getLogger(__name__).info("Removing temporary %r from sys.path", turcar_container)
        del sys.path[0]

    target_cwd = sys.argv[1]
    options = ast.literal_eval(sys.argv[2])
    report_time("Before constructing backend")
    # Don't introduce new variables after constructing the backend, as it cleaned the main scope
    MainCPythonBackend(target_cwd, options).mainloop()
