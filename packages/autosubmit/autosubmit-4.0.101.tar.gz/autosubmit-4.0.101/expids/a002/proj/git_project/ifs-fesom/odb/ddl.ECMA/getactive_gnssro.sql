//
//-- ODB/SQL file 'getactive_gnssro.sql'
//
//   Last updated:  16-Mar-2011
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where gnssro.len@hdr are > 0 :
SAFEGUARD;

CREATE VIEW getactive_gnssro AS
  SELECT target, seqno, "*@gnssro"
    FROM index, hdr, sat, gnssro
   WHERE obstype = $limb
     AND codetype = $gpsro
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1 AND distribtype IS NOT NULL) )
;
