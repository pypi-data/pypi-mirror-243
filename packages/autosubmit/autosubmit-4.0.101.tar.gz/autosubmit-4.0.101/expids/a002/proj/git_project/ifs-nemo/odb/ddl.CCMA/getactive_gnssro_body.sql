//
//-- ODB/SQL file 'getactive_gnssro_body.sql'
//
//   Last updated:  16-Mar-2011
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_gnssro_body AS
  SELECT target, seqno, "*@gnssro_body"
    FROM index, hdr, sat, gnssro, gnssro_body, body
   WHERE obstype = $limb
     AND codetype = $gpsro
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
     AND  gnssro_body.len > 0
     AND  gnssro_body.len == body.len
;
