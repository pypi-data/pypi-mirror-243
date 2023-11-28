//
//-- ODB/SQL file 'getactive_gbrad_body.sql'
//
//   Last updated:  22-Jul-2010
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_gbrad_body AS
  SELECT target, seqno, "*@gbrad_body"
    FROM index, hdr, gbrad, gbrad_body, body
   WHERE obstype = $gbrad
     AND codetype = $radrr
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
     AND  gbrad_body.len > 0
     AND  gbrad_body.len == body.len
;
