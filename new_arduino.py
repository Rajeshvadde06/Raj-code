import serial
import time

# Replace with your actual port name (e.g., 'COM3' for Windows, '/dev/ttyUSB0' for Linux)
arduino_port = 'COM6'
baud_rate = 9600

# Establish serial connection
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Wait for Arduino to reset
    print("Connected to Arduino.")

    while True:
        print("\nCommands:\n 1. s,<time_in_sec>\n 2. stop\n 3. config\n 4. exit")
        user_input = input("Enter command: ").strip().lower()

        if user_input == "exit":
            print("Exiting program.")
            break

        ser.write((user_input + '\n').encode())  # Send to Arduino
        print("Command sent. Waiting for response...\n")

        # Reading response from Arduino
        while ser.in_waiting:
            response = ser.readline().decode().strip()
            if response:
                print("Arduino:", response)

except serial.SerialException:
    print(f"Could not open port {arduino_port}. Is it correct?")
except KeyboardInterrupt:
    print("\nProgram interrupted.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")
