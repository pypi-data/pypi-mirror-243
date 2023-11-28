//
//-- ODB/SQL file 'obsdist_radar_body.sql'
//
//   Created:  22-Jun-2009
//

READONLY;
NOREORDER; // Do not change the given table order in FROM-statement (important)

SET $pe = 0;
SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;
SET $hdr_min = -1;

CREATE VIEW obsdist_radar_body AS
  SELECT distribid, seqno, window_offset, "*@radar_body"
    FROM hdr, sat, radar, radar_body
   WHERE obstype = $radar
     AND 1 <= distribid
     AND  distribtype = 1
     AND  radar_body.len > 0
     AND  radar_body.len == body.len
     AND (obstype = $obstype OR $obstype = -1 )
     AND (codetype = $codetype OR $codetype = -1)
     AND (sensor = $sensor OR $sensor = -1)
     AND (window_offset = $hdr_min OR $hdr_min = -1)
     AND paral($pe, distribid)
;
