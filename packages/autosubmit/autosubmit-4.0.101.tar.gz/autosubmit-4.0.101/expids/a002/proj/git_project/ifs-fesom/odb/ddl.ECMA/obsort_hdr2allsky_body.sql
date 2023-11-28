//
//-- ODB/SQL file 'obsort_hdr2allsky_body.sql'
//
//   Last updated:  18-May-2001
//

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW obsort_hdr2allsky_body AS
  SELECT target, seqno
    FROM index, hdr, sat, radiance, allsky, body, allsky_body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
     AND (#allsky_body >= 1)
     AND (allsky_body.len@allsky > 0)
     AND (obstype = $allsky AND codetype = $ssmi)
     ORDERBY seqno
;
