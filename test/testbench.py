from myhdl import block, always, instance, Signal, intbv, delay, ResetSignal, always_seq, always_comb, StopSimulation

# Defining encryption/decryption module
@block
def tt_um_opt_encryptor(ui_in, uo_out, uio_in, uio_out, uio_oe, ena, clk, rst_n):
  
    data = Signal(intbv(0)[8:]) #signal declarations 
    pad_read = Signal(intbv(0)[8:])#intbv = integer bit
    pad_gen = Signal(intbv(0)[8:])
    decrypt = Signal(bool(0))
    out = Signal(intbv(0)[8:])

    @always_comb
    def assign():
        data.next = ui_in
        decrypt.next = uio_in[0]
        uio_oe.next = 0b11110000
        uio_out.next = intbv(0)[8:]  # Reset uio_out

    @always_seq(clk.posedge, reset=ResetSignal(rst_n, active=0, async=True))
    def logic():
        if ena:
            out.next = pad_read ^ data if decrypt else pad_gen ^ data
        else:
            out.next = 0
    uo_out.next = out

    return assign, logic

# Testbench for simulations
@block
def testbench():
    # Define signals
    reset, clock, ena, rst_n = [Signal(bool(0)) for _ in range(4)]
    ui_in, uio_in = [Signal(intbv(0)[8:]) for _ in range(2)]
    uo_out, uio_out, uio_oe = [Signal(intbv(0)[8:]) for _ in range(3)]

    encryptor = tt_um_opt_encryptor(ui_in, uo_out, uio_in, uio_out, uio_oe, ena, clock, rst_n)

    # Clock generation
    @always(delay(5))
    def clock_gen():
        clock.next = not clock

    # Test cases
    @instance
    def simulate():
        # Reset
        reset.next = 1
        rst_n.next = 0
        yield delay(10)
        reset.next = 0
        rst_n.next = 1

        # Simulate encryption
        ena.next = 1
        ui_in.next = 0xFF
        uio_in.next = 2  # Example for setting up encryption
        yield clock.posedge

        # Simulate decryption
        ui_in.next = 0x00
        uio_in.next = 130  # Example for setting up decryption
        yield clock.posedge

        # Finish simulation
        raise StopSimulation

    return encryptor, clock_gen, simulate

# Run the testbench
if __name__ == "__main__":
    tb = testbench()
    tb.run_sim()
