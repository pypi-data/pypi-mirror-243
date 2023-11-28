//
//-- ODB/SQL file 'getactive_ssmi.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & ssmi.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW getactive_ssmi AS
  SELECT target, seqno, "*@ssmi"
    FROM index, hdr, sat, ssmi
   WHERE obstype = $satem
     AND codetype = $ssmi
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1 AND distribtype IS NOT NULL) )
;
