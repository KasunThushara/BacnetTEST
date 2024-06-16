import time
import random
from bacpypes.object import ScheduleObject
from bacpypes.primitivedata import Real
import BAC0
from BAC0.core.devices.local.models import analog_input, analog_output
from BAC0.core.devices.local.object import ObjectFactory


# Define a function to create and add BACnet objects
def define_objects(device):
    ObjectFactory.clear_objects()
    _new_objects=analog_input(
        instance=10,
        description="Temperature",
        properties={"units": "degreesCelsius"},
        name="Temperature",
        presentValue=18.0,
    )
    analog_input(
        instance=20,
        description="Humidity",
        properties={"units": "degreesCelsius"},
        name="Humidity",
        presentValue=58.0,
    )

    return _new_objects.add_objects_to_application(device)


# Connect to the BACnet device
device1 = BAC0.connect(ip='192.168.8.106/24', port='47808', deviceId='1110')

# Define and add the objects to the device
define_objects(device1)

# Main loop to update sensor values
try:
    while True:
        device1["Temperature"].presentValue = round(random.uniform(5, 35), 2)
        device1["Humidity"].presentValue = round(random.uniform(30, 70), 2)

        print(f"Device Temperature: {device1['Temperature'].presentValue} °C")
        print(f"Device Humidity: {device1['Humidity'].presentValue} %")

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping the BACnet device...")
    device1.disconnect()
