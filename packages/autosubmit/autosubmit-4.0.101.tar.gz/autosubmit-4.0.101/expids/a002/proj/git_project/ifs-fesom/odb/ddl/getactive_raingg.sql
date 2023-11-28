//
//-- ODB/SQL file 'getactive_raingg.sql'
//
//   Last updated:  22-Jul-2010
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where raingg.len@hdr are > 0 :
SAFEGUARD;

CREATE VIEW getactive_raingg AS
  SELECT target, seqno, "*@raingg"
    FROM index, hdr, raingg
   WHERE obstype = $raingg
     AND codetype = $radrr
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1 AND distribtype IS NOT NULL)
	  OR ($all = 2 ) )
;
