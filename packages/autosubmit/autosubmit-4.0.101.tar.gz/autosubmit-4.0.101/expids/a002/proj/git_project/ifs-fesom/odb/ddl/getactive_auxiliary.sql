//
//-- ODB/SQL file 'getactive_auxiliary.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_auxiliary AS
  SELECT target, seqno, "*@auxiliary"
    FROM index, hdr, sat, auxiliary, body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
     AND  auxiliary.len > 0
     AND  auxiliary.len == body.len
;
