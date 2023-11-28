//
//-- ODB/SQL file 'obsdist_hdr2allsky_body.sql'
//
//   Created:  22-Jun-2009
//

READONLY;

SET $pe = 0;
SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;
SET $hdr_min = -1; // contains window offset

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW obsdist_hdr2allsky_body AS
  SELECT distribid, seqno, window_offset
    FROM hdr, allsky, allsky_body
       WHERE 1 <= distribid
       AND distribtype = 1
       AND (#allsky_body >= 1)
       AND (obstype = $obstype OR $obstype = -1)
       AND (codetype = $codetype OR $codetype = -1)
       AND (sensor = $sensor OR $sensor = -1)
       AND (window_offset = $hdr_min OR $hdr_min = -1)
       AND (obstype = $allsky) AND (codetype = $ssmi)
       AND  allsky_body.len > 0
       AND  allsky_body.len == body.len
       AND  paral($pe, distribid)
;
