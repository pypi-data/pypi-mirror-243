//
//-- ODB/SQL file 'getactive_radar_body.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_radar_body AS
  SELECT target, seqno, "*@radar_body"
    FROM index, hdr, sat, radar, radar_body, body
   WHERE obstype = $radar
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
     AND  radar_body.len > 0
     AND  radar_body.len == body.len
;
