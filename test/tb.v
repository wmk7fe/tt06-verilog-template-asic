`default_nettype none `timescale 1ns / 1ps

/* This testbench just instantiates the module and makes some convenient wires
   that can be driven / tested by the cocotb test.py.
*/
module tb ();
  // Dump the signals to a VCD file. You can view it with gtkwave.
  initial begin
    $dumpfile("tb.vcd");
    $dumpvars(0, tb);
    #1;
  end
   
  // Wire up the inputs and outputs:
  reg clk;
  reg rst_n;
  reg ena;
  reg [3:0] uio_in_upper;
  wire [7:0] uo_out;
  wire uio_out_upper;
  wire [3:0] uio_out_lower; 
  wire [7:0] uio_oe;

  reg [7:0] data;
  reg [2:0] r_num;
  reg decrypt;

  wire [7:0] out;
  wire [2:0] index_out;

  // Replace tt_um_example with your module name:
  tt_um_opt_encryptor user_project (

      // Include power ports for the Gate Level test:
`ifdef GL_TEST
      .VPWR(1'b1),
      .VGND(1'b0),
`endif

      .ui_in  (data),    // Dedicated inputs
      .uo_out (out),   // Dedicated outputs
      .uio_in ({uio_in_upper, r_num, decrypt}),   // IOs: Input path
      .uio_out({uio_out_upper, index_out, uio_out_lower}),  // IOs: Output path
      .uio_oe (uio_oe),   // IOs: Enable path (active high: 0=input, 1=output)
      .ena    (ena),      // enable - goes high when design is selected
      .clk    (clk),      // clock
      .rst_n  (rst_n)     // not reset
  );


   initial $monitor($time,,"[%b]\t%b\tq=%b || data_in %b, data_out %b, index_in %b, index_out %b, enable %b, decrypt enable %b, clk %b",clk,ui_in[0],uo_out, data, out, r_num, index_out, ena, decrypt, clk);

   
endmodule


