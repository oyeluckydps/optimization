// Benchmark "demo_addition_results" written by ABC on Tue Jun 24 11:19:00 2025

module demo_addition_results ( 
    op1_7, op1_6, op1_5, op1_4, op1_3, op1_2, op1_1, op1_0, op2_7, op2_6,
    op2_5, op2_4, op2_3, op2_2, op2_1, op2_0,
    result_7, result_6, result_5, result_4, result_3, result_2, result_1,
    result_0  );
  input  op1_7, op1_6, op1_5, op1_4, op1_3, op1_2, op1_1, op1_0, op2_7,
    op2_6, op2_5, op2_4, op2_3, op2_2, op2_1, op2_0;
  output result_7, result_6, result_5, result_4, result_3, result_2, result_1,
    result_0;
  assign result_2 = ~op1_7 & ~op1_6 & ~op1_5 & ~op1_4 & ~op2_7 & ~op2_6 & ~op2_5 & ~op2_4 & (~op1_3 | (op1_3 & (~op2_3 | (op2_3 & ((op1_2 & (op1_1 ? (((op2_2 ^ op2_1) & (~op1_0 | (op1_0 & ~op2_0))) | (op1_0 & op2_0 & (~op2_2 | (op2_2 & op2_1)))) : (op1_0 ? ((op2_2 & (~op2_1 | (op2_1 & ~op2_0))) | (op2_1 & op2_0)) : op2_2))) | (op2_2 & ((op1_0 & ((op1_1 & (~op2_1 ^ ~op2_0)) | (~op1_2 & op2_1 & op2_0))) | (op1_1 & ~op1_0 & op2_1))))))));
  assign result_1 = ~op1_7 & ~op1_6 & ~op1_5 & ~op1_4 & ~op2_7 & ~op2_6 & ~op2_5 & ~op2_4 & (op1_3 ? ((op2_3 & ((((op1_1 & ~op1_0 & op2_1) | (op1_0 & ((op2_1 & op2_0) | (op1_1 & (~op2_1 ^ ~op2_0))))) & (~op1_2 ^ op2_2)) | ((~op1_0 | (op1_0 & ~op2_0)) & ((op2_2 & op2_1 & ~op1_2 & ~op1_1) | (op1_2 & op1_1 & ~op2_2 & ~op2_1))) | (op1_0 & ((op1_2 & ~op1_1 & ~op2_2 & (~op2_1 | (op2_1 & ~op2_0))) | (~op1_2 & op1_1 & op2_2 & ~op2_1 & ~op2_0))) | (op1_2 & ~op1_1 & ~op1_0 & ~op2_2))) | ((op1_2 ? ~op2_3 : (op2_2 & ~op2_1)) & (~op1_1 | (op1_1 & ~op1_0))) | (~op2_3 & ((op1_1 & (((~op2_2 | (op2_2 & op2_1)) & (op1_2 ? op1_0 : op2_0)) | (op1_0 & op2_2 & ~op2_1) | (~op1_2 & op2_1 & ~op2_0))) | (~op1_2 & ~op1_1 & op2_1)))) : ((~op1_1 & (op1_2 | (~op1_2 & op1_0 & op2_3 & op2_1))) | (~op1_0 & (op1_2 ? op1_1 : (op2_3 & op2_2))) | (~op2_3 & (~op1_2 | (op1_2 & op1_1 & op1_0))) | (op2_3 & ((op1_1 & ((~op1_2 & ~op2_2) | (op1_0 & ((op2_2 & op2_1) | (op1_2 & (~op2_2 | (op2_2 & ~op2_1))))))) | (op2_2 & ~op2_1 & ~op1_2 & op1_0)))));
  assign result_0 = ~op1_7 & ~op1_6 & ~op1_5 & ~op1_4 & ~op2_7 & ~op2_6 & ~op2_5 & ~op2_4 & (op1_3 ? ((op1_2 & ((op2_2 & ((op1_1 & ((~op1_0 & op2_3 & ~op2_1) | (op2_1 & ~op2_0 & op1_0 & ~op2_3))) | (~op2_3 & ((~op1_1 & ~op2_1) | (op1_0 & op2_1 & op2_0))) | (~op1_1 & op2_1 & (op2_0 ? ~op1_0 : op2_3)))) | (~op2_3 & (op1_1 ? (~op1_0 | (op1_0 & ~op2_2)) : (op2_1 & ~op2_0))) | (~op1_1 & op2_3 & ~op2_2 & op2_1 & (~op1_0 | (op1_0 & ~op2_0))))) | (~op1_2 & ((~op1_0 & (op1_1 ? (op2_2 & ~op2_1) : (op2_3 & op2_1))) | (~op1_1 & ((~op2_3 & op2_2) | (op2_1 & ~op2_0 & op1_0 & op2_3))) | (op1_1 & ~op2_3 & ((op2_1 & (op2_0 | (op2_2 & ~op2_0))) | (~op2_2 & ~op2_0))))) | (op2_0 & ((~op1_1 & ((~op2_3 & ~op2_2) | (op1_0 & op2_3 & ~op2_1))) | (op2_3 & op2_1 & op1_1 & op1_0))) | (op1_1 & ~op2_1 & (op1_0 ? (op2_3 ? ~op2_0 : op2_2) : (op2_3 & ~op2_2)))) : ((~op1_1 & (op1_2 | (~op1_2 & op1_0 & op2_3 & ~op2_1))) | (~op1_0 & (op1_2 ? op1_1 : (op2_3 & op2_1))) | (op1_1 & ((op1_0 & ((op2_3 & ~op2_2) | (op1_2 & (~op2_3 | (op2_3 & op2_2))))) | (op2_2 & ~op2_1 & ~op1_2 & op2_3))) | (~op1_2 & (~op2_3 | (op2_2 & op2_1 & op1_0 & op2_3)))));
  assign result_7 = 1'b0;
  assign result_6 = 1'b0;
  assign result_5 = 1'b0;
  assign result_4 = 1'b0;
  assign result_3 = 1'b0;
endmodule


