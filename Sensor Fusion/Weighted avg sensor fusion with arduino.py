import serial.tools.list_ports

# List and select the port for Arduino
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []

for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(f"Selected Port: {portVar}")

serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()


# Weighted Average Fusion Function
def weighted_average_fusion(sensor_data, weights):
    fused_value = 0  # Initialize fused value
    for reading, weight in zip(sensor_data, weights):
        fused_value += reading * weight
    return fused_value


# Define weights for temperature and humidity
temperature_weights = [0.4, 0.3, 0.2, 0.1]
humidity_weights = [0.3, 0.3, 0.2, 0.2]

print("Waiting for sensor data...")

while True:
    if serialInst.in_waiting:
        # Read data from the serial port
        packet = serialInst.readline().decode('utf').strip()


        try:
            # split the data
            temp_data_str, hum_data_str = packet.split(" HUM:")
            temp_data_str = temp_data_str.replace("TEMP:", "")

            temperature_readings = list(map(float, temp_data_str.split(",")))
            humidity_readings = list(map(float, hum_data_str.split(",")))

            # Validate data lengths
            if len(temperature_readings) != len(temperature_weights) or len(humidity_readings) != len(humidity_weights):
                print("Error: Mismatch between readings and weights.")
                continue

            # Calculate fused values
            fused_temperature = weighted_average_fusion(temperature_readings, temperature_weights)
            fused_humidity = weighted_average_fusion(humidity_readings, humidity_weights)

            # Output results
            print(f"Fused Temperature: {fused_temperature:.2f}°C")
            print(f"Fused Humidity: {fused_humidity:.2f}%")

        except Exception as e:
            print(f"Error parsing data: {e}")
