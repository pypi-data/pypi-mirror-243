//
//-- ODB/SQL file 'obsort_satob.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & satob.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW obsort_satob AS
  SELECT target, seqno, "*@satob"
    FROM index, hdr, sat, satob
   WHERE obstype = $satob
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  paral($pe, target)
     ORDERBY seqno
;
