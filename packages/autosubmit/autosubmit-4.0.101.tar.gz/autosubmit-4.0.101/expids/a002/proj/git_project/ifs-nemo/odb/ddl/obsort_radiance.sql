//
//-- ODB/SQL file 'obsort_radiance.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & radiance.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW obsort_radiance AS
  SELECT target, seqno, "*@radiance"
    FROM index, hdr, sat, radiance
   WHERE (obstype = $satem OR obstype = $allsky)
     AND (codetype = $ssmi OR codetype = $atovs)
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  paral($pe, target)
     ORDERBY seqno
;
