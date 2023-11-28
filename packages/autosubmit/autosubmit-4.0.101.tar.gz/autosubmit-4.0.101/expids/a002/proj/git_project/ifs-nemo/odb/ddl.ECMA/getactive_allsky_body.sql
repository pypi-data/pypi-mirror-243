//
//-- ODB/SQL file 'getactive_allsky_body.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_allsky_body AS
  SELECT target, seqno, "*@allsky_body"
    FROM index, hdr, sat, radiance, allsky, allsky_body, body
   WHERE obstype = $allsky
     AND codetype = $ssmi
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
     AND  allsky_body.len > 0
     AND  allsky_body.len == body.len
;
