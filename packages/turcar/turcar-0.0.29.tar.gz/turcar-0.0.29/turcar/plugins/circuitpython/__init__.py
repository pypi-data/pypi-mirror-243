from turcar.languages import tr
from turcar.plugins.circuitpython.cirpy_front import CircuitPythonConfigPage, CircuitPythonProxy
from turcar.plugins.micropython import add_micropython_backend


def load_plugin():
    add_micropython_backend(
        "CircuitPython",
        CircuitPythonProxy,
        tr("CircuitPython (generic)"),
        CircuitPythonConfigPage,
        sort_key="50",
    )
