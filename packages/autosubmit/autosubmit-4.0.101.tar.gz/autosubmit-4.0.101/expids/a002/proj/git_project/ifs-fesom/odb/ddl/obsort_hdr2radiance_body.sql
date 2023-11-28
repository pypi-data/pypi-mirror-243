//
//-- ODB/SQL file 'obsort_hdr2radiance_body.sql'
//
//   Last updated:  18-Mar-2011
//

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW obsort_hdr2radiance_body AS
  SELECT target, seqno
    FROM index, hdr, sat, radiance, body, radiance_body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
     AND (#radiance_body >= 1)
     AND (radiance_body.len@radiance > 0)
     AND ((obstype = $satem OR obstype = $allsky)
           AND (codetype = $ssmi OR codetype = $atovs))
     ORDERBY seqno
;
