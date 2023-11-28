// add sat table to have satellite_identifier@sat
CREATE VIEW cycle_biasprep_robhdr AS
SELECT  
   body.len,codetype, satellite_identifier@sat, sensor,         //  table hdr
   date, time, lat, lon                      //  table hdr
FROM  hdr, sat
WHERE  (obstype = $satem)
 AND   (codetype = $atovs)
