//
//-- ODB/SQL file 'getactive_raingg_body.sql'
//
//   Last updated:  22-Jul-2010
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_raingg_body AS
  SELECT target, seqno, "*@raingg_body"
    FROM index, hdr, raingg, raingg_body, body
   WHERE obstype = $raingg
     AND codetype = $radrr
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL)
	  OR ($all = 2 ) )
     AND  raingg_body.len > 0
     AND  raingg_body.len == body.len
;
