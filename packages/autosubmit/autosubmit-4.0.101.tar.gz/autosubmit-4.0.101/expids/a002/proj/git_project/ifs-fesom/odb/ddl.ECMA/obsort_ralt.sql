//
//-- ODB/SQL file 'obsort_ralt.sql'
//
//   Last updated:  14 August 20146
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & ralt.len@sat are > 0 :
SAFEGUARD;

//  SELECT target, seqno, "*@ralt"
CREATE VIEW obsort_ralt  AS
  SELECT target, seqno
    FROM index, hdr, body, sat 
   WHERE obstype = $ralt
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  paral($pe, target)
;
