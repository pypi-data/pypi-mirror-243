//
//-- ODB/SQL file 'obsort_collocated_imager_information.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & collocated_imager_information.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW obsort_collocated_imager_information AS
  SELECT target, seqno, "*@collocated_imager_information"
    FROM index, hdr, sat, radiance, collocated_imager_information
   WHERE obstype = $satem
     AND codetype = $atovs
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  paral($pe, target)
     AND collocated_imager_information.len > 0
     AND collocated_imager_information.len == radiance.len
     ORDERBY seqno
;
