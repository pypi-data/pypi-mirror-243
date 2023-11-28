//
//-- ODB/SQL file 'obsdist_raingg_body.sql'
//
//   Created:  22-Jul-2010
//

READONLY;
NOREORDER; // Do not change the given table order in FROM-statement (important)

SET $pe = 0;
SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;
SET $hdr_min= -1; // contains window offset

CREATE VIEW obsdist_raingg_body AS
  SELECT distribid, seqno, window_offset, "*@raingg_body"
    FROM hdr, raingg, raingg_body
   WHERE obstype = $raingg
     AND codetype = $radrr
     AND (obstype = $obstype OR $obstype = -1 )
     AND (codetype = $codetype OR $codetype = -1)
     AND (sensor = $sensor OR $sensor = -1)
     AND (window_offset = $hdr_min OR $hdr_min = -1)
     AND 1 <= distribid
     AND distribtype = 1
     AND raingg_body.len > 0
     AND raingg_body.len == body.len
     AND paral($pe, distribid)
;
