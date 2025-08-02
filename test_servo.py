# test_servo.py
import time
from lerobot.motors.feetech import FeetechMotorsBus
from lerobot.motors import Motor, MotorNormMode

# --- Configuration ---
# IMPORTANT: Replace 'COMx' with the serial port of your ESP32-C3.
# On Windows, it will be 'COM3', 'COM4', etc.
# On Linux, it's typically '/dev/ttyACM0'.
# On macOS, '/dev/cu.usbmodem...'.
# You can find the correct port in the Arduino IDE or by running:
# python -m serial.tools.list_ports
SERIAL_PORT = 'COM12' 

# We'll define one motor for this test.
# The default ID for a new Feetech servo is 1.
# The model is 'sts3215'. We use RAW mode to send integer positions.
MOTORS = {
    "test_motor": Motor(id=1, model="sts3215", norm_mode=MotorNormMode.RANGE_0_100)
}

def main():
    """Connects to the servo, pings it, and commands it to move."""
    print(f"Attempting to connect to motor bus on port {SERIAL_PORT}...")
    bus = None  # Initialize bus to None
    try:
        # The FeetechMotorsBus handles the low-level communication
        bus = FeetechMotorsBus(port=SERIAL_PORT, motors=MOTORS)
        print("✅ Connection successful.")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        print("\nPlease check the following:")
        print("  1. Your ESP32 is connected and the firmware is running.")
        print("  2. The SERIAL_PORT in this script is correct.")
        print("  3. The servo has external power and its GND is connected to the ESP32's GND.")
        print("  4. The servo's data line (white wire) is connected to GPIO21.")
        return

    try:
        # --- Test 1: Ping the motor ---
        # This sends a simple instruction packet and waits for a reply.
        print("\n--- Test 1: Pinging motor with ID 1 ---")
        bus.ping("test_motor")
        print("✅ Ping successful! The motor responded.")

        # --- Test 2: Read Present Position ---
        # This sends a READ instruction and prints the response.
        print("\n--- Test 2: Reading Present Position ---")
        position = bus.read("Present_Position", "test_motor")
        print(f"✅ Motor is at position: {position}")

        # --- Test 3: Move the motor ---
        # This sends two WRITE instructions to the 'Goal_Position' register.
        print("\n--- Test 3: Moving motor to two different positions ---")
        # The STS3215 position range is 0-4095
        target_pos_1 = 50    # Center position (50% of 0-100 range)
        target_pos_2 = 25    # Another position (25% of 0-100 range)
        
        print(f"  - Sending motor to position {target_pos_1}...")
        bus.write("Goal_Position", "test_motor", target_pos_1)
        time.sleep(2) # Wait for the motor to physically move

        print(f"  - Sending motor to position {target_pos_2}...")
        bus.write("Goal_Position", "test_motor", target_pos_2)
        time.sleep(2)

        print("\n✅ Test script finished successfully.")

    except Exception as e:
        print(f"\n❌ An error occurred during testing: {e}")
        print("This could be due to wiring issues, an incorrect motor ID, or power problems.")

    finally:
        # Disconnect cleanly to release the serial port
        if bus and bus.is_connected:
            bus.disconnect()
            print("\nDisconnected from motor bus.")

if __name__ == "__main__":
    main()
