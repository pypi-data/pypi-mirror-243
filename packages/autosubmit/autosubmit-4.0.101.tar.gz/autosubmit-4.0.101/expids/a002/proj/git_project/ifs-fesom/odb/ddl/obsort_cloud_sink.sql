//
//-- ODB/SQL file 'obsort_cloud_sink.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & cloud_sink.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW obsort_cloud_sink AS
  SELECT target, seqno, "*@cloud_sink"
    FROM index, hdr, sat, radiance, cloud_sink
   WHERE obstype = $satem
     AND (codetype = $ssmi OR codetype = $atovs)
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND  paral($pe, target)
     ORDERBY seqno
;
