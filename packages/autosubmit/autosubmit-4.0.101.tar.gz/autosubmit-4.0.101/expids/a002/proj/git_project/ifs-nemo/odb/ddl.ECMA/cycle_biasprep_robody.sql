CREATE VIEW cycle_biasprep_robody AS
SELECT entryno,
   varno, vertco_reference_1, obsvalue, biascorr, fg_depar, an_depar  //  table body
FROM  index, hdr, body
WHERE  (obstype = $satem)
 AND   (codetype = $atovs)
