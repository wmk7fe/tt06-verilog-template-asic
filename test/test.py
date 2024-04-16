import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from cocotb.binary import BinaryValue



@cocotb.test()
async def test_otp_encryptor(dut):
    clk = dut.clk
    clock = Clock(clk, 10, units="ns")
    
    ena = dut.ena
    data_in = dut.ui_in
    data_out = dut.uo_out
    decrypt = dut.uio_in[0]
    rnum_in = dut.uio_in[3:1]
    rnum_out = dut.uio_out[6:4]
    rst_n = dut.rst_n
    
    rst_n.value = Force(1)
    ena.value = Force(0)
    data_in.value = Force(0)
    decrypt.value = Force(0)
    rnum_in.value = Force(0)

    await(ClockCycles(clk, 1))

    rst_n.value = Force(0)

    await(ClockCycles(clk, 1))

    rst_n.value = Force(1)

    await(ClockCycles(clk, 1))

    data_in.value = Force(0xab)
    ena.value = Force(1)
    await(ClockCycles(dut.clk, 1))

    ena.value = Force(0)
    data = data_out.value
    rnum = rnum_out.value
    dut._log.info(f'Encrypted output: {data} ({rnum})')
