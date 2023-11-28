//
//-- ODB/SQL file 'getactive_sat.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_sat AS
  SELECT target, seqno, "*@sat"
    FROM index, hdr, sat
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1 AND distribtype IS NOT NULL) )
     AND  sat.len == 1
;
