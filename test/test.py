import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from cocotb.binary import BinaryValue
from cocotb.handle import Force



@cocotb.test()
async def test_otp_encryptor(dut):
    clk = dut.clk
    clock = Clock(clk, 10, units="ns")
    
    ena = dut.ena
    data_in = dut.ui_in
    data_out = dut.uo_out
    rnum_decrypt_in = dut.uio_in
    rnum_out = dut.uio_out
    rst_n = dut.rst_n
    
    rst_n.value = Force(1)
    ena.value = Force(0)
    data_in.value = Force(0)
    rnum_decrypt_in.value = Force(0)

    await(ClockCycles(clk, 1))

    rst_n.value = Force(0)

    await(ClockCycles(clk, 1))

    rst_n.value = Force(1)

    await(ClockCycles(clk, 1))

    data_in.value = Force(0xab)
    ena.value = Force(1)
    
    await(ClockCycles(clk, 1))

    dut._log.info(f'Encryptor  input: {data_in.value}')

    await(ClockCycles(clk, 1))
    
    data = data_out.value
    rnum = rnum_out.value >> 4
    dut._log.info(f'Encrypted output: {data_out.value} ({rnum_out.value >> 4})')

    await(ClockCycles(clk,1))

    decrypt = 1
    data_in.value = Force(data)
    rnum_decrypt_in.value = Force((rnum << 1) + decrypt)

    await(ClockCycles(clk, 1))

    dut._log.info(f'Decryptor  input: {data_in.value} ({rnum_decrypt_in.value})')

    await(ClockCycles(clk, 5))

    data = data_out.value
    dut._log.info(f'Decrypted output: {data_out.value}')

    await(ClockCycles(clk, 1))

    dut._log.info(f'({data})')

    
