//
//-- ODB/SQL file 'getactive_radar_station.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where sat.len@hdr & radar_station.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW getactive_radar_station AS
  SELECT target, seqno, "*@radar_station"
    FROM index, hdr, sat, radar_station
   WHERE obstype = $radar
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1 AND distribtype IS NOT NULL) )
;
