//
//-- ODB/SQL file 'obsort_smos.sql'
//
//   Last updated:  20-Jul-2013
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & smos.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW obsort_smos AS
  SELECT target, seqno, "*@smos"
    FROM index, hdr, sat, smos
   WHERE obstype = $satem 
     AND codetype = 400
     AND (   ($all = 1)
      OR ($all = 0 AND report_status.active = 1)
      OR ($all = 2 ) )
     AND  paral($pe, target)
     ORDERBY seqno
;

