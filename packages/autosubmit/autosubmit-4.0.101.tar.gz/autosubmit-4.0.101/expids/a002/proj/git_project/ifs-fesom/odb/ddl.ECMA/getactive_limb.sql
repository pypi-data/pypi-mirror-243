//
//-- ODB/SQL file 'getactive_limb.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & limb.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW getactive_limb AS
  SELECT target, seqno, "*@limb"
    FROM index, hdr, sat, limb
   WHERE obstype = $limb
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1 AND distribtype IS NOT NULL) )
;
