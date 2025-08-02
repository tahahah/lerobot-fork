import time
from lerobot.motors import FeetechMotorsBus, Motor, MotorNormMode

# --- Configuration ---
SERIAL_PORT = 'COM11'
MOTOR_ID = 1

def main():
    """Connects to the bus and repeatedly pings a motor to generate TX traffic."""
    print(f"Attempting to connect to motor bus on port {SERIAL_PORT}...")

    # We define a dummy motor. The script doesn't require a real motor to be connected,
    # as we are only checking for data transmission (TX) from the ESP32.
    motors = {
        "led_test_motor": Motor(id=MOTOR_ID, model="sts3215", norm_mode=MotorNormMode.RANGE_0_100)
    }

    try:
        bus = FeetechMotorsBus(port=SERIAL_PORT, motors=motors)
        print("✅ Connection successful.")
        print(f"Continuously pinging motor ID {MOTOR_ID} on GPIO21. Check for LED activity.")
        print("Press Ctrl+C to stop.")

        while True:
            # This will continuously send a ping command out on the serial port.
            # We don't care about the response for this test.
            bus.ping(MOTOR_ID)
            time.sleep(0.05)  # 50ms delay between pings

    except KeyboardInterrupt:
        print("\nStopping test.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        if 'bus' in locals() and bus.is_connected:
            bus.disconnect()
            print("Disconnected.")

if __name__ == "__main__":
    main()
