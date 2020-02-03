import config
import util
import camera

from logzero import logger, logfile
from sense_hat import SenseHat
from datetime import datetime, timedelta
from time import sleep

sh = SenseHat()

# Configure logging
logfile(util.path_for(config.LOGFILE))

# Configure runtime
start_time = datetime.now()
end_time = start_time + timedelta(minutes=config.RUNTIME)

logger.info(f'Starting logging at {start_time}')
logger.info(f'Will log for {config.RUNTIME} minutes ({end_time})')

# Configure CSV
csvfile = util.path_for_data(1)
logger.info(f'Logging to {csvfile}')
# TODO write header

while True:
    # Check for end time
    now = datetime.now()
    if now >= end_time:
        logger.info(f'Finished run at {now}')
        break

    # Main loop
    try:
        orientation = sh.get_orientation_degrees()
        compass = sh.get_compass()
        compass_raw = sh.get_compass_raw()
        gyro = sh.get_gyroscope()
        gyro_raw = sh.get_gyroscope_raw()
        camera.capture(debug_capture=True)


        util.add_csv_data(csvfile, (
            now,
            sh.get_humidity(),
            sh.get_temperature(),
            sh.get_temperature_from_humidity(),
            sh.get_temperature_from_pressure(),
            sh.get_pressure(),
            orientation['roll'],
            orientation['pitch'],
            orientation['yaw'],
            compass,
            compass_raw['x'],
            compass_raw['y'],
            compass_raw['z'],
            gyro['roll'],
            gyro['pitch'],
            gyro['yaw'],
            gyro_raw['x'],
            gyro_raw['y'],
            gyro_raw['z'],
        ))
    except Exception as e:
        logger.error('{}: {})'.format(e.__class__.__name__, e))

    sleep(config.SLEEPTIME)
