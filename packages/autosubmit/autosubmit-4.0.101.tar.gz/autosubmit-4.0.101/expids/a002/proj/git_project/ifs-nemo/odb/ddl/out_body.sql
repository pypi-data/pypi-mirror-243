SET $utc = -1;

SET $varno = -1;

SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;

SET $press = -1;

CREATE VIEW out_body AS
  SELECT boxid,  // Must be the first entry
         orography, // Must be the second entry
         "*@body"
    FROM desc, hdr, modsurf,body
   WHERE utc = $utc
     AND varno = $varno
     AND (obstype = $obstype OR $obstype = -1)
     AND (codetype = $codetype OR $codetype = -1)
     AND (sensor = $sensor OR $sensor = -1)
     AND (vertco_reference_1 = $press)
;
