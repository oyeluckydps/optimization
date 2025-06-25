// Benchmark "demo_addition_results" written by ABC on Wed Jun 25 08:07:16 2025

module demo_addition_results ( 
    op1_7, op1_6, op1_5, op1_4, op1_3, op1_2, op1_1, op1_0, op2_7, op2_6,
    op2_5, op2_4, op2_3, op2_2, op2_1, op2_0,
    result_7, result_6, result_5, result_4, result_3, result_2, result_1,
    result_0  );
  input  op1_7, op1_6, op1_5, op1_4, op1_3, op1_2, op1_1, op1_0, op2_7,
    op2_6, op2_5, op2_4, op2_3, op2_2, op2_1, op2_0;
  output result_7, result_6, result_5, result_4, result_3, result_2, result_1,
    result_0;
  wire new_n30, new_n31, new_n32, new_n33, new_n34, new_n35, new_n36,
    new_n37, new_n38, new_n39, new_n40, new_n41, new_n42, new_n43, new_n44,
    new_n45, new_n46, new_n47, new_n48, new_n49, new_n51, new_n52, new_n53,
    new_n54, new_n55, new_n56, new_n57, new_n58, new_n59, new_n60, new_n61,
    new_n62, new_n63, new_n64, new_n65, new_n66, new_n67, new_n68, new_n69,
    new_n70, new_n71, new_n72, new_n73, new_n74, new_n75, new_n76, new_n77,
    new_n78, new_n79, new_n80, new_n81, new_n82, new_n83, new_n84, new_n85,
    new_n86, new_n87, new_n88, new_n89, new_n90, new_n91, new_n92, new_n93,
    new_n95, new_n96, new_n97, new_n98, new_n99, new_n100, new_n101,
    new_n102, new_n103, new_n104, new_n105, new_n106, new_n107, new_n108,
    new_n109, new_n110, new_n111, new_n112, new_n113, new_n114, new_n115,
    new_n116, new_n117, new_n118, new_n119, new_n120, new_n121;
  nor4  g00(.dina(op2_4), .dinb(op2_5), .dinc(op2_6), .dind(op2_7), .dout(new_n30));
  not   g01(.din(new_n30), .dout(new_n31));
  nor4  g02(.dina(op1_4), .dinb(op1_5), .dinc(op1_6), .dind(op1_7), .dout(new_n32));
  not   g03(.din(new_n32), .dout(new_n33));
  nor2  g04(.dina(new_n33), .dinb(new_n31), .dout(new_n34));
  nand2 g05(.dina(op2_1), .dinb(op1_1), .dout(new_n35));
  not   g06(.din(new_n35), .dout(new_n36));
  nand2 g07(.dina(op2_0), .dinb(op1_0), .dout(new_n37));
  not   g08(.din(new_n37), .dout(new_n38));
  nor2  g09(.dina(new_n38), .dinb(new_n36), .dout(new_n39));
  nor2  g10(.dina(op2_2), .dinb(op1_2), .dout(new_n40));
  not   g11(.din(new_n40), .dout(new_n41));
  nor2  g12(.dina(op2_1), .dinb(op1_1), .dout(new_n42));
  not   g13(.din(new_n42), .dout(new_n43));
  nand2 g14(.dina(new_n43), .dinb(new_n41), .dout(new_n44));
  nor2  g15(.dina(new_n44), .dinb(new_n39), .dout(new_n45));
  not   g16(.din(new_n45), .dout(new_n46));
  nand2 g17(.dina(op2_2), .dinb(op1_2), .dout(new_n47));
  nand4 g18(.dina(new_n47), .dinb(new_n46), .dinc(op2_3), .dind(op1_3), .dout(new_n48));
  nand2 g19(.dina(new_n48), .dinb(new_n34), .dout(new_n49));
  not   g20(.din(new_n49), .dout(result_2));
  not   g21(.din(op1_3), .dout(new_n51));
  not   g22(.din(new_n39), .dout(new_n52));
  not   g23(.din(new_n44), .dout(new_n53));
  nand3 g24(.dina(new_n47), .dinb(new_n53), .dinc(new_n52), .dout(new_n54));
  nor2  g25(.dina(new_n42), .dinb(new_n39), .dout(new_n55));
  not   g26(.din(new_n55), .dout(new_n56));
  not   g27(.din(op1_2), .dout(new_n57));
  nor2  g28(.dina(op2_2), .dinb(new_n57), .dout(new_n58));
  not   g29(.din(new_n58), .dout(new_n59));
  nand2 g30(.dina(new_n59), .dinb(new_n56), .dout(new_n60));
  nand2 g31(.dina(new_n60), .dinb(new_n54), .dout(new_n61));
  not   g32(.din(new_n61), .dout(new_n62));
  nor3  g33(.dina(new_n42), .dinb(new_n38), .dinc(new_n36), .dout(new_n63));
  not   g34(.din(new_n63), .dout(new_n64));
  nand3 g35(.dina(op2_2), .dinb(op2_3), .dinc(new_n57), .dout(new_n65));
  nor2  g36(.dina(new_n65), .dinb(new_n64), .dout(new_n66));
  not   g37(.din(op2_3), .dout(new_n67));
  nand2 g38(.dina(op1_0), .dinb(op1_1), .dout(new_n68));
  not   g39(.din(new_n68), .dout(new_n69));
  nor2  g40(.dina(op2_1), .dinb(op1_2), .dout(new_n70));
  not   g41(.din(new_n70), .dout(new_n71));
  nor2  g42(.dina(new_n71), .dinb(new_n69), .dout(new_n72));
  nor2  g43(.dina(new_n72), .dinb(new_n67), .dout(new_n73));
  not   g44(.din(new_n73), .dout(new_n74));
  not   g45(.din(op1_1), .dout(new_n75));
  not   g46(.din(op2_0), .dout(new_n76));
  nor3  g47(.dina(new_n76), .dinb(op2_3), .dinc(new_n75), .dout(new_n77));
  nor3  g48(.dina(op2_1), .dinb(op2_2), .dinc(op1_2), .dout(new_n78));
  not   g49(.din(new_n78), .dout(new_n79));
  nor2  g50(.dina(new_n79), .dinb(new_n77), .dout(new_n80));
  not   g51(.din(new_n80), .dout(new_n81));
  nand2 g52(.dina(new_n81), .dinb(new_n74), .dout(new_n82));
  not   g53(.din(new_n82), .dout(new_n83));
  nor4  g54(.dina(new_n83), .dinb(new_n66), .dinc(new_n62), .dind(new_n51), .dout(new_n84));
  nand3 g55(.dina(op2_3), .dinb(new_n57), .dinc(new_n51), .dout(new_n85));
  not   g56(.din(op1_0), .dout(new_n86));
  not   g57(.din(op2_1), .dout(new_n87));
  nor3  g58(.dina(new_n87), .dinb(new_n86), .dinc(op1_1), .dout(new_n88));
  nor2  g59(.dina(op2_2), .dinb(op1_1), .dout(new_n89));
  not   g60(.din(new_n89), .dout(new_n90));
  nor3  g61(.dina(new_n90), .dinb(new_n88), .dinc(new_n85), .dout(new_n91));
  not   g62(.din(new_n91), .dout(new_n92));
  nand2 g63(.dina(new_n92), .dinb(new_n34), .dout(new_n93));
  nor2  g64(.dina(new_n93), .dinb(new_n84), .dout(result_1));
  nand2 g65(.dina(new_n64), .dinb(op2_3), .dout(new_n95));
  nor2  g66(.dina(new_n76), .dinb(op2_1), .dout(new_n96));
  not   g67(.din(new_n96), .dout(new_n97));
  nand2 g68(.dina(new_n97), .dinb(op1_1), .dout(new_n98));
  nor2  g69(.dina(op2_2), .dinb(op2_3), .dout(new_n99));
  nand2 g70(.dina(new_n99), .dinb(new_n98), .dout(new_n100));
  nand2 g71(.dina(new_n100), .dinb(new_n95), .dout(new_n101));
  not   g72(.din(new_n77), .dout(new_n102));
  nand2 g73(.dina(new_n102), .dinb(new_n64), .dout(new_n103));
  not   g74(.din(new_n103), .dout(new_n104));
  nor2  g75(.dina(new_n104), .dinb(new_n57), .dout(new_n105));
  not   g76(.din(new_n105), .dout(new_n106));
  nor2  g77(.dina(new_n42), .dinb(new_n36), .dout(new_n107));
  nand2 g78(.dina(op2_3), .dinb(op1_0), .dout(new_n108));
  nor2  g79(.dina(new_n108), .dinb(new_n107), .dout(new_n109));
  nor3  g80(.dina(op2_2), .dinb(op2_3), .dinc(op1_1), .dout(new_n110));
  nor2  g81(.dina(new_n110), .dinb(new_n109), .dout(new_n111));
  not   g82(.din(new_n111), .dout(new_n112));
  nand2 g83(.dina(new_n112), .dinb(op2_0), .dout(new_n113));
  nand4 g84(.dina(new_n113), .dinb(new_n106), .dinc(new_n101), .dind(op1_3), .dout(new_n114));
  not   g85(.din(new_n114), .dout(new_n115));
  not   g86(.din(new_n34), .dout(new_n116));
  nor2  g87(.dina(op2_1), .dinb(op1_0), .dout(new_n117));
  nor2  g88(.dina(new_n117), .dinb(new_n88), .dout(new_n118));
  nor3  g89(.dina(new_n118), .dinb(new_n85), .dinc(new_n53), .dout(new_n119));
  nor2  g90(.dina(new_n119), .dinb(new_n116), .dout(new_n120));
  not   g91(.din(new_n120), .dout(new_n121));
  nor2  g92(.dina(new_n121), .dinb(new_n115), .dout(result_0));
  zero  g93(.dout(result_7));
  zero  g94(.dout(result_6));
  zero  g95(.dout(result_5));
  zero  g96(.dout(result_4));
  zero  g97(.dout(result_3));
endmodule


