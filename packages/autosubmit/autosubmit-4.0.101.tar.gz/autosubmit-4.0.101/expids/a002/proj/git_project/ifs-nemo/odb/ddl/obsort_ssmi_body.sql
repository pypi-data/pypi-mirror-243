//
//-- ODB/SQL file 'obsort_ssmi_body.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_ssmi_body AS
  SELECT target, seqno, "*@ssmi_body"
    FROM index, hdr, sat, ssmi, ssmi_body, body
   WHERE obstype = $satem
     AND codetype = $ssmi
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
     AND  ssmi_body.len > 0
     AND  ssmi_body.len == body.len
     ORDERBY seqno
;
