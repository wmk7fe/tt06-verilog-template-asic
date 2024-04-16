import cocotb
from cocotb.triggers import FallingEdge, Timer


async def generate_clock(dut):
    """Generate clock pulses."""

    for cycle in range(100):
        dut.clk.value = 0
        await Timer(1, units="ns")
        dut.clk.value = 1
        await Timer(1, units="ns")


@cocotb.test()
async def test_otp_encyrptor(dut):
    """Try accessing the design."""

    clk = dut.clk
    ena = dut.ena
    data_in = dut.ui_in
    data_out = dut.uo_out
    rnum_decrypt_in = dut.uio_in
    rnum_out = dut.uio_out
    rst_n = dut.rst_n

    rst_n.value = 1
    ena.value = 0
    data_in.value = 0
    rnum_decrypt_in.value = 0
    
    await cocotb.start(generate_clock(dut))  # run the clock "in the background"

    await Timer(5, units="ns")  # wait a bit
    await FallingEdge(dut.clk)  # wait for falling edge/"negedge"

    rst_n.value = 0

    await FallingEdge(dut.clk)

    rst_n.value = 1

    await FallingEdge(clk)

    data = 0xab

    for i in range(9):
        await FallingEdge(clk)
        ena.value = 1
        decrypt = 0
        data_in.value = data
        rnum_decrypt_in.value = decrypt
        
        await FallingEdge(clk)
        
        ena.value = 0
        dut._log.info(f'Encryptor  input: {data_in.value}')
        data = data_out.value
        rnum = rnum_out.value >> 4
        dut._log.info(f'Encrypted output: {data_out.value} ({rnum_out.value >> 4})')
    
        await FallingEdge(clk)
    
        decrypt = 1
        ena.value = 1
        data_in.value = (data)
        rnum_decrypt_in.value = ((rnum << 1) + decrypt)
    
        await FallingEdge(clk)
    
        ena.value = 0
        data = data_out.value
        dut._log.info(f'Decryptor  input: {data_in.value} ({rnum_decrypt_in.value})')
        dut._log.info(f'Decryptor output: {data_out.value}')
    
        await FallingEdge(clk)

    
