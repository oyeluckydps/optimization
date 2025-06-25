// Benchmark "demo_addition_results" written by ABC on Wed Jun 25 07:41:45 2025

module demo_addition_results ( 
    op1_7, op1_6, op1_5, op1_4, op1_3, op1_2, op1_1, op1_0, op2_7, op2_6,
    op2_5, op2_4, op2_3, op2_2, op2_1, op2_0,
    result_7, result_6, result_5, result_4, result_3, result_2, result_1,
    result_0  );
  input  op1_7, op1_6, op1_5, op1_4, op1_3, op1_2, op1_1, op1_0, op2_7,
    op2_6, op2_5, op2_4, op2_3, op2_2, op2_1, op2_0;
  output result_7, result_6, result_5, result_4, result_3, result_2, result_1,
    result_0;
  wire new_n26, new_n27, new_n28, new_n29, new_n30, new_n31, new_n32,
    new_n33, new_n34, new_n35, new_n36, new_n37, new_n38, new_n39, new_n40,
    new_n41, new_n42, new_n43, new_n45, new_n46, new_n47, new_n48, new_n49,
    new_n50, new_n51, new_n52, new_n53, new_n54, new_n55, new_n56, new_n57,
    new_n58, new_n59, new_n60, new_n61, new_n62, new_n63, new_n64, new_n65,
    new_n66, new_n67, new_n68, new_n69, new_n70, new_n71, new_n72, new_n73,
    new_n74, new_n75, new_n77, new_n78, new_n79, new_n80, new_n81, new_n82,
    new_n83, new_n84, new_n85, new_n86, new_n87, new_n88, new_n89, new_n90,
    new_n91, new_n92, new_n93, new_n94, new_n95, new_n96, new_n97, new_n98,
    new_n99, new_n100, new_n101, new_n102, new_n103, new_n104, new_n105;
  assign new_n26 = ~op1_7 & ~op1_6;
  assign new_n27 = ~op1_5 & ~op1_4;
  assign new_n28 = ~op2_7 & ~op2_6;
  assign new_n29 = ~op2_5 & ~op2_4;
  assign new_n30 = new_n28 & new_n29;
  assign new_n31 = new_n26 & new_n27;
  assign new_n32 = new_n30 & new_n31;
  assign new_n33 = ~op1_2 & ~op2_2;
  assign new_n34 = ~op1_1 & ~op2_1;
  assign new_n35 = op1_1 & op2_1;
  assign new_n36 = op1_0 & op2_0;
  assign new_n37 = ~new_n35 & ~new_n36;
  assign new_n38 = ~new_n34 & ~new_n37;
  assign new_n39 = ~new_n33 & new_n38;
  assign new_n40 = op1_2 & op2_2;
  assign new_n41 = op1_3 & op2_3;
  assign new_n42 = ~new_n40 & new_n41;
  assign new_n43 = ~new_n39 & new_n42;
  assign result_2 = new_n32 & ~new_n43;
  assign new_n45 = op1_2 & ~op2_2;
  assign new_n46 = ~new_n38 & ~new_n45;
  assign new_n47 = new_n39 & ~new_n40;
  assign new_n48 = ~new_n46 & ~new_n47;
  assign new_n49 = ~op1_2 & op2_3;
  assign new_n50 = op1_1 & op1_0;
  assign new_n51 = op2_2 & ~op2_1;
  assign new_n52 = ~op2_0 & new_n51;
  assign new_n53 = new_n50 & new_n52;
  assign new_n54 = ~op1_1 & op2_1;
  assign new_n55 = op2_2 & ~new_n36;
  assign new_n56 = new_n54 & new_n55;
  assign new_n57 = ~new_n53 & ~new_n56;
  assign new_n58 = new_n49 & ~new_n57;
  assign new_n59 = ~op1_2 & ~op2_1;
  assign new_n60 = ~new_n50 & new_n59;
  assign new_n61 = op2_3 & ~new_n60;
  assign new_n62 = op1_1 & ~op2_3;
  assign new_n63 = op2_0 & new_n62;
  assign new_n64 = ~op2_2 & new_n59;
  assign new_n65 = ~new_n63 & new_n64;
  assign new_n66 = ~new_n61 & ~new_n65;
  assign new_n67 = op1_3 & ~new_n66;
  assign new_n68 = ~new_n58 & new_n67;
  assign new_n69 = ~new_n48 & new_n68;
  assign new_n70 = op1_0 & op2_1;
  assign new_n71 = ~op1_3 & ~op1_1;
  assign new_n72 = ~op2_2 & new_n71;
  assign new_n73 = new_n49 & ~new_n70;
  assign new_n74 = new_n72 & new_n73;
  assign new_n75 = new_n32 & ~new_n74;
  assign result_1 = ~new_n69 & new_n75;
  assign new_n77 = ~new_n34 & ~new_n35;
  assign new_n78 = op1_0 & op2_3;
  assign new_n79 = ~new_n77 & new_n78;
  assign new_n80 = ~op2_3 & ~op2_2;
  assign new_n81 = ~op1_1 & new_n80;
  assign new_n82 = ~new_n79 & ~new_n81;
  assign new_n83 = op2_0 & ~new_n82;
  assign new_n84 = ~op1_0 & op2_3;
  assign new_n85 = op2_0 & ~new_n84;
  assign new_n86 = new_n54 & ~new_n85;
  assign new_n87 = ~new_n63 & ~new_n86;
  assign new_n88 = op1_2 & ~new_n87;
  assign new_n89 = ~op2_1 & op2_0;
  assign new_n90 = op1_1 & ~new_n89;
  assign new_n91 = new_n80 & ~new_n90;
  assign new_n92 = ~new_n36 & new_n77;
  assign new_n93 = op2_3 & ~new_n92;
  assign new_n94 = ~new_n91 & ~new_n93;
  assign new_n95 = op1_3 & ~new_n83;
  assign new_n96 = ~new_n88 & ~new_n94;
  assign new_n97 = new_n95 & new_n96;
  assign new_n98 = ~op1_0 & ~op2_1;
  assign new_n99 = ~op1_1 & new_n70;
  assign new_n100 = ~new_n98 & ~new_n99;
  assign new_n101 = op2_2 & ~new_n34;
  assign new_n102 = ~op1_3 & new_n49;
  assign new_n103 = ~new_n101 & new_n102;
  assign new_n104 = ~new_n100 & new_n103;
  assign new_n105 = new_n32 & ~new_n104;
  assign result_0 = ~new_n97 & new_n105;
  assign result_7 = 1'b0;
  assign result_6 = 1'b0;
  assign result_5 = 1'b0;
  assign result_4 = 1'b0;
  assign result_3 = 1'b0;
endmodule


