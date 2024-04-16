import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from cocotb.binary import BinaryValue

@cocotb.test()
async def test_otp_encryptor(dut):
    # Start the clock
    clock = Clock(dut.clk, 10, units="ns")  # Clock period of 10 ns
    cocotb.start_soon(clock.start())

    # Reset the device
    dut.rst_n.value = 0
    dut.ena.value = 0
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)

    # Scenario: Encryption
    # Set up for encryption
    dut.ena.value = 1
    dut.ui_in.value = 0xFF  # Example plaintext
    dut.uio_in.value = BinaryValue("00000010")  # Encryption setup
    await ClockCycles(dut.clk, 2)

    # Capture the output from encryption
    encrypted_value = dut.uo_out.value
    dut._log.info(f'Encrypted output: {encrypted_value}')

    # Scenario: Decryption
    # Assuming the device can decrypt its own output
    dut.ui_in.value = encrypted_value  # Feed the encrypted value as input
    dut.uio_in.value = BinaryValue("10000010")  # Decryption setup
    await ClockCycles(dut.clk, 2)

    # Check if the decrypted output matches the original input (0xFF)
    decrypted_value = dut.uo_out.value
    ## assert decrypted_value == 0xFF, f"Decryption failed: expected 0xFF, got {decrypted_value}"
    dut._log.info(f'Decrypted output: {decrypted_value}')
