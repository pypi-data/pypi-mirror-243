CREATE VIEW cycle_biasprep_sathdr AS
SELECT 
   scanpos@radiance,                                           //  table radiance
FROM  hdr, sat, radiance
WHERE  (obstype = $satem)
 AND   (codetype = $atovs)
