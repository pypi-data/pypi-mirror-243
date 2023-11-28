//
//-- ODB/SQL file 'getactive_scatt_body.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_scatt_body AS
  SELECT target, seqno, "*@scatt_body"
    FROM index, hdr, sat, scatt, scatt_body, body
   WHERE obstype = $scatt
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
     AND  scatt_body.len > 0
     AND  scatt_body.len == body.len

;
