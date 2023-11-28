//
//-- ODB/SQL file 'getactive_hdr2radar_body.sql'

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW getactive_hdr2radar_body AS
  SELECT target, seqno
   FROM index, hdr, sat, radar, body, radar_body
   WHERE (   ($all = 1)
          OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
     AND (#radar_body >= 1)
     AND (radar_body.len@radar > 0)
     AND (obstype = $radar)
;
