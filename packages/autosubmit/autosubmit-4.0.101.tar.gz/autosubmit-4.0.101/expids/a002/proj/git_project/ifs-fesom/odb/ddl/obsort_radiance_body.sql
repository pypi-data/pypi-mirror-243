//
//-- ODB/SQL file 'obsort_radiance_body.sql'
//
//   Last updated:  22-Mar-2011
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_radiance_body AS
  SELECT target, seqno, "*@radiance_body"
    FROM index, hdr, sat, radiance, radiance_body, body
   WHERE (obstype = $satem OR obstype = $allsky)
     AND (codetype = $ssmi OR codetype = $atovs)
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
     AND  radiance_body.len > 0
     AND  radiance_body.len == body.len
     ORDERBY seqno
;
