//
//-- ODB/SQL file 'getactive_allsky.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & allsky.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW getactive_allsky AS
  SELECT target, seqno, "*@allsky"
    FROM index, hdr, sat, radiance, allsky
   WHERE obstype = $allsky
     AND codetype = $ssmi
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1 AND distribtype IS NOT NULL) )
;
