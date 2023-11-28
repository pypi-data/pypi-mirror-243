//
//-- ODB/SQL file 'obsort_resat_averaging_kernel.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_resat_averaging_kernel AS
  SELECT target, seqno, "*@resat_averaging_kernel"
    FROM index, hdr, sat, resat, resat_averaging_kernel, body
   WHERE obstype = $satem
     AND (codetype = $resat)
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
     AND  resat_averaging_kernel.len > 0
     AND  resat_averaging_kernel.len == body.len
     ORDERBY seqno
;
