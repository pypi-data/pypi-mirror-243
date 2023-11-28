//
//-- ODB/SQL file 'obsort_scatt.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & scatt.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW obsort_scatt AS
  SELECT target, seqno, "*@scatt"
    FROM index, hdr, sat, scatt
   WHERE obstype = $scatt
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  paral($pe, target)
     ORDERBY seqno
;
