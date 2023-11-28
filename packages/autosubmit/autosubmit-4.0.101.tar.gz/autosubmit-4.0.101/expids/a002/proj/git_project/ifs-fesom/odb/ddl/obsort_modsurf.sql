//
//-- ODB/SQL file 'obsort_modsurf.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_modsurf AS
  SELECT target, seqno, "*@modsurf"
    FROM index, hdr, modsurf
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  modsurf.len == 1
     AND  paral($pe, target)
     ORDERBY seqno
;
