//
//-- ODB/SQL file 'obsort_hdr2gnssro_body.sql'
//
//   Last updated:  16-Mar-2011
//

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW obsort_hdr2gnssro_body AS
  SELECT target, seqno
    FROM index, hdr, sat, gnssro, body, gnssro_body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
     AND (#gnssro_body >= 1)
     AND (gnssro_body.len@gnssro > 0)
     AND (obstype = $limb AND codetype = $gpsro)
     ORDERBY seqno
;
