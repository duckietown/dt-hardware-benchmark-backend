from scipy import interpolate

def measurements(data_latency, data_segments, data_sd_card):
    return {
        'diagnostics': {
            'resources_stats': [
                {
                    'name': 'Memory in Percent',
                    'ylabel': 'RAM',
                    'ylim': (0, 100),
                    'keys': ['memory.used', 'memory.total'],
                    'calc': lambda x, y: 100 * x / y,
                    'export_name': 'ram_p',
                    'unit': '%',

                },
                {
                    'name': 'Swap in Percent',
                    'ylabel': 'Swap',
                    'ylim': (0, 100),
                    'keys': ['swap.used', 'swap.total'],
                    'calc': lambda x, y: 100 * x / y,
                    'export_name': 'swap_p',
                    'unit': '%',
                },
                {
                    'name': 'CPU Percent',
                    'ylabel': 'CPU',
                    'ylim': (0, 100),
                    'keys': ['cpu.pcpu'],
                    'export_name': 'cpu_p',
                    'unit': '%',
                },
            ],
            'health': [
                {
                    'name': 'Status',
                    'ylabel': 'Status [ok, warn, error]',
                    'ylim': (0, 2),
                    'format': lambda x: 2 if x == 'error' else 1 if x == 'warning' else 0,
                    'keys': ['status'],
                    'export_name': 'status_tribool',
                    'unit': ' ',
                    'ip': lambda x, y: interpolate.interp1d(x, y, bounds_error=False),
                    'avg_multiplier': 50,
                    #'avg_weigh_lower': True
                },
                {
                    'name': 'CPU Temperature',
                    'ylabel': 'CPU',
                    'ylim': (0, 100),
                    'format': lambda i: i[0:-2],
                    'keys': ['temp'],
                    'export_name': 'cpu_temp_c',
                    'unit': '°C',
                },
                {
                    'name': 'Core Voltage',
                    'ylabel': 'Core',
                    'ylim': (0, 1.5),
                    'format': lambda i: i[0:-1],
                    'keys': ['volts.core'],
                    'export_name': 'cpu_core_v',
                    'unit': 'V',
                    'avg_weigh_lower': True,
                    'avg_multiplier': 100/1.5,
                },
                {
                    'name': 'Throttling',
                    'ylabel': 'Throttling [yes/no]',
                    'ylim': (0, 1),
                    'format': lambda x: 1 if x else 0,
                    'keys': ['throttled_humans.throttling-now'],
                    'export_name': 'throttling_bool',
                    'unit': ' ',
                    'ip': lambda x, y: interpolate.interp1d(x, y, bounds_error=False),
                    'avg_multiplier': 100,
                },
                {
                    'name': 'Core Clock',
                    'ylabel': 'Core',
                    'ylim': (0, 600),
                    'calc': lambda x: x / 1000000,
                    'keys': ['clock.core'],
                    'export_name': 'cpu_core_clock',
                    'unit': 'MHz',
                    'avg_multiplier': 1/6,
                },
                {
                    'name': 'ARM Clock',
                    'ylabel': 'ARM',
                    'ylim': (0, 2000),
                    'calc': lambda x: x / 1000000,
                    'keys': ['clock.arm'],
                    'export_name': 'cpu_arm_clock',
                    'unit': '?',
                    'avg_multiplier': 1/20,
                },
            ],
            'containers_cfg': [
                {
                    'base_name': ' Threads',
                    'ylabel': 'Threads',
                    'keys': 'process_stats.nthreads',
                    'unit': '#',
                },

                {
                    'base_name': ' CPU in Percent',
                    'ylabel': 'CPU',
                    'keys': 'container_stats.pcpu',
                    'unit': '%',
                }
            ],
            'extern': [
                {
                    'name': 'Lane detector node latency',
                    'data': data_latency,
                    'ylabel': 'Latency',
                    'ylim': (0, 1000),
                    't0': min(data_latency.get('time')),
                    'keys': ['meas'],
                    'export_name': 'ldn_latency',
                    'unit': 'ms',
                    'ip': lambda x, y: interpolate.interp1d(x, y, bounds_error=False),
                    'avg_multiplier': .1,
                },
                {
                    'name': 'Detected Segments',
                    'data': data_segments,
                    'ylabel': 'Segments',
                    't0': min(data_segments.get('time')),
                    'keys': ['meas'],
                    'export_name': 'ldn_segments',
                    'unit': '#',
                    'ip': lambda x, y: interpolate.interp1d(x, y, bounds_error=False),
                    'avg_multiplier': 100/75,
                },
                {
                    'name': 'SD-Card Write Speed',
                    'data': data_sd_card,
                    'ylabel': 'Write Speed',
                    'notime': True,
                    'keys': ['write'],
                    'export_name': 'sd_card_write_speed',
                    'unit': 'MB/s',
                    'avg_multiplier': 10,
                    'avg_weigh_lower': True,
                },
                {
                    'name': 'SD-Card Read Speed',
                    'data': data_sd_card,
                    'ylabel': 'Write Speed',
                    'notime': True,
                    'keys': ['read'],
                    'export_name': 'sd_card_read_speed',
                    'unit': 'MB/s',
                    'avg_multiplier': 10,
                    'avg_weigh_lower': True,
                },
            ]
        },
    }

meta = {
    'time': 'general.time_iso',
    'target': 'general.target',
    'duration': 'general.duration',
    'cores': 'endpoint.NCPU',
    'mem': 'endpoint.MemTotal'
}