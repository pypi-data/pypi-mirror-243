//
//-- ODB/SQL file 'obsdist_poolno.sql'
//
//   Created:  22-Jun-2009
//

READONLY; // the view is treated as read/only

SET $obstype=-1;
SET $codetype = -1;
SET $sensor = -1;
SET $hdr_min = -1;

CREATE VIEW obsdist_poolno AS
  SELECT distinct procid                //  r/o
    FROM index, hdr
    WHERE (obstype = $obstype OR $obstype = -1 )
          AND (codetype = $codetype OR $codetype = -1)
          AND (sensor = $sensor OR $sensor = -1)
          AND (window_offset = $hdr_min OR $hdr_min = -1)
;
