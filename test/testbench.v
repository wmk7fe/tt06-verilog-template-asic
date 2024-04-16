`timescale 1ns / 1ps
module testbench;

    // Signals for tt_um_opt_encryptor
    reg [7:0] ui_in;
    wire [7:0] uo_out;
    reg [7:0] uio_in;
    wire [7:0] uio_out;
    wire [7:0] uio_oe;
    reg ena;
    reg clk;
    reg rst_n;

    // Instantiate the encryptor
    tt_um_opt_encryptor encryptor (
        .ui_in(ui_in),
        .uo_out(uo_out),
        .uio_in(uio_in),
        .uio_out(uio_out),
        .uio_oe(uio_oe),
        .ena(ena),
        .clk(clk),
        .rst_n(rst_n)
    );

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    //  scenarios
    initial begin
        // Initialize all signals
        rst_n = 0; ena = 0; ui_in = 0; uio_in = 0;
        #10;
        rst_n = 1;  // Release reset

        // encryption
        ena = 1; ui_in = 8'hFF; uio_in = 8'b00000010; // Set up encryption
        #20;

        //decryption
        ui_in = 8'h00; uio_in = 8'b10000010; // Set up decryption

        #100;
        $finish; // End simulation after 100 ns
    end

endmodule
