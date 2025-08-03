import serial
import time
import argparse

# --- IMPORTANT: THIS IS SET VIA COMMAND LINE ARGUMENT ---
# Example: /dev/tty.usbmodem5A460843021
# --------------------------------------------------------

BAUD_RATES = [1000000, 500000, 250000, 115200]
BROADCAST_ID = 0xFE

# Feetech SCS/STS Ping Instruction Packet
# [0xFF, 0xFF, ID, Length, Instruction, Param1, ..., ParamN, Checksum]
ping_instruction = [0xFF, 0xFF, BROADCAST_ID, 0x02, 0x01]
checksum = (~(BROADCAST_ID + 0x02 + 0x01)) & 0xFF
ping_instruction.append(checksum)

packet_to_send = bytearray(ping_instruction)

def perform_loopback_test(port_name):
    print("\n--- Starting Loopback Test ---")
    print("Instructions: Disconnect motors and connect a wire between TX and RX on your USB adapter.")
    input("Press Enter to continue once you have connected the TX and RX pins...")

    test_string = b'Hello, world!'
    # Use a common baud rate for the test
    baud = 115200

    try:
        with serial.Serial(port_name, baud, timeout=0.5) as ser:
            print(f"Port {port_name} opened successfully at {baud} bps.")
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            print(f"Sending: {test_string}")
            ser.write(test_string)

            time.sleep(0.1)
            response = ser.read(len(test_string))

            if response == test_string:
                print(f"SUCCESS! Received: {response}")
                print("Loopback test passed. Your USB-to-serial adapter is working correctly.")
                return True
            else:
                print(f"FAILURE. Received: {response}. Expected: {test_string}")
                print("Loopback test failed. Check your adapter or the TX/RX jumper wire.")
                return False

    except serial.SerialException as e:
        print(f"Error during loopback test: {e}")
        return False

def test_motors(port_name):
    print("\n--- Starting Motor Ping Test ---")
    print("Instructions: Connect the motors to your USB adapter and ensure they are POWERED ON.")
    input("Press Enter to continue...")

    for baud in BAUD_RATES:
        print(f"\n--- Testing Baud Rate: {baud} ---")
        try:
            with serial.Serial(port_name, baud, timeout=0.1) as ser:
                print(f"Port {port_name} opened successfully at {baud} bps.")
                ser.reset_input_buffer()
                ser.reset_output_buffer()

                print(f"Sending Ping Packet: {list(packet_to_send)}")
                ser.write(packet_to_send)

                time.sleep(0.1)
                response = ser.read(128)  # Read up to 128 bytes

                if response:
                    print(f"SUCCESS! Received {len(response)} bytes: {list(response)}")
                    print("This means at least one motor is alive and responding at this baud rate.")
                    return True
                else:
                    print("No response received.")

        except serial.SerialException as e:
            print(f"Error opening port {port_name}: {e}")
            return False

    print("\n--- Motor Test Complete: No motors detected. ---")
    print("This confirms the issue is likely with motor power or the wiring to the motors.")
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Feetech Motor and Serial Port Diagnostic Tool.')
    parser.add_argument('port', type=str, help='The serial port to test (e.g., /dev/tty.usbmodem12345).')
    parser.add_argument('--test', type=str, choices=['loopback', 'motors'], required=True, help='The test to run: \'loopback\' or \'motors\'.')
    args = parser.parse_args()

    if args.test == 'loopback':
        perform_loopback_test(args.port)
    elif args.test == 'motors':
        test_motors(args.port)
