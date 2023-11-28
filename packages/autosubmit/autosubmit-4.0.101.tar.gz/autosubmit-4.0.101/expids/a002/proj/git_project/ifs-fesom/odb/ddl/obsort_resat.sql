//
//-- ODB/SQL file 'obsort_resat.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & resat.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW obsort_resat AS
  SELECT target, seqno, "*@resat"
    FROM index, hdr, sat, resat
   WHERE obstype = $satem
     AND (codetype = $resat)
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  paral($pe, target)
     ORDERBY seqno
;
