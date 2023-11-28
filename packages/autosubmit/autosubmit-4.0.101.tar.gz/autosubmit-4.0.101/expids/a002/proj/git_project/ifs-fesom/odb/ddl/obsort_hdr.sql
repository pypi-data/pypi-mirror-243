//
//-- ODB/SQL file 'obsort_hdr.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_hdr AS
  SELECT target, seqno, "*@hdr"
    FROM index, hdr
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  paral($pe, target)
     ORDERBY seqno
;
