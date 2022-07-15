from python_jbdtool_bms import BMS
from prometheus_client import start_http_server, Gauge
import time

g_total_voltage = Gauge("jbd_bms_total_voltage", "Total Voltage")
g_current = Gauge(
    "jbd_bms_current", "Current in Ah, positive is charging, negative is discharging"
)
g_residual_capacity = Gauge("jbd_bms_residual_capacity", "Residual Capacity in Ah")
g_nominal_capacity = Gauge("jbd_bms_nominal_capacity", "Nominal Capacity in Ah")
g_rsoc = Gauge(
    "jbd_bms_relative_state_of_charge", "Relative State of Charge in percent"
)
g_number_of_cells = Gauge("jbd_bms_number_of_cells", "Number of Cells")
g_cycle_times = Gauge("jbd_bms_cycle_times", "Cycle count")
g_cell_voltages = Gauge("jbd_bms_cell_voltages", "Cell Voltage", ['cell'])


def get_jbd_metrics():
    bms = BMS("/dev/ttyUSB0")
    bms.query_all()

    g_total_voltage.set(bms.total_voltage)
    g_current.set(bms.current)
    g_residual_capacity.set(bms.residual_capacity)
    g_nominal_capacity.set(bms.nominal_capacity)
    g_rsoc.set(bms.rsoc)
    g_number_of_cells.set(bms.number_of_cells)
    g_cycle_times.set(bms.cycle_times)

    for i in range(len(bms.cell_voltages)):
        g_cell_voltages.labels(cell=i).set(bms.cell_voltages[i])


if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8080)
    # Generate some requests.
    while True:
        get_jbd_metrics()
        time.sleep(10)
