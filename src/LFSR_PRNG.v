module LFSR_PRNG (
    clk,
    rst,
    prn);

    input clk;
    input rst;
    output [7:0] prn;

    reg [15:0] D16 = 6'd1; //NEVER 000000

    assign prn[0] = D16[15];
    assign prn[1] = D16[13];
    assign prn[2] = D16[11];
	 assign prn[3] = D16[9];
	 assign prn[4] = D16[7];
	 assign prn[5] = D16[5];
	 assign prn[6] = D16[3];
	 assign prn[7] = D16[1];

    always @ (posedge rst or posedge clk)
    if (rst)
        begin
            D16 <= 16'd1;
        end
    else
        begin
            D16[1] <= D16[0];
            D16[2] <= D16[1];
            D16[3] <= D16[2];
            D16[4] <= D16[3];
            D16[5] <= D16[4];
				D16[6] <= D16[5];
				D16[7] <= D16[6];
				D16[8] <= D16[7];
				D16[9] <= D16[8];
				D16[10] <= D16[9];
				D16[11] <= D16[10];
				D16[12] <= D16[11];
				D16[13] <= D16[12];
				D16[14] <= D16[13];
				D16[15] <= D16[14];
            D16[0] <= D16[15] ^ D16[14];
        end
		  
endmodule
