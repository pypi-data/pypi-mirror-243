//
//-- ODB/SQL file 'obsort_sat.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_sat AS
  SELECT target, seqno, "*@sat"
    FROM index, hdr, sat
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  sat.len == 1
     AND  paral($pe, target)
     ORDERBY seqno
;
