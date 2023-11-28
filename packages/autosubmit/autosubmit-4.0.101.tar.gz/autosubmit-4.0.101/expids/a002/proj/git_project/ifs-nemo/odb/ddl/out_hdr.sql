SET $utc = -1;

SET $varno = -1;

SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;

CREATE VIEW out_hdr AS
  SELECT "*@hdr" // boxid@hdr is implicitly the first entry
    FROM desc, hdr
   WHERE utc = $utc
     AND varno = $varno
     AND (obstype = $obstype OR $obstype = -1)
     AND (codetype = $codetype OR $codetype = -1)
     AND (sensor = $sensor OR $sensor = -1)
;
