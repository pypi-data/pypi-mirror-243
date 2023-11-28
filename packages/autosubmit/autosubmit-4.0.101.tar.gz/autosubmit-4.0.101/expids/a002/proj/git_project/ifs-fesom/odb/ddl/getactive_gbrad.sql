//
//-- ODB/SQL file 'getactive_gbrad.sql'
//
//   Last updated:  22-Jul-2010
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where gbrad.len@hdr are > 0 :
SAFEGUARD;

CREATE VIEW getactive_gbrad AS
  SELECT target, seqno, "*@gbrad"
    FROM index, hdr, gbrad
   WHERE obstype = $gbrad
     AND codetype = $radrr
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1 AND distribtype IS NOT NULL) )
;
