//
//-- ODB/SQL file 'sathdr_radar.sql'
//
//   Last updated:  24-May-2000
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sathdr_radar AS
  SELECT seqno  READONLY,         // r/o; MUST BECOME FIRST
      stalt@radar_station,         // r/o
      satellite_identifier@sat,
      lat@radar_station, // r/o
      lon@radar_station, // r/o
      antenht@radar_station, // r/o
      ident@radar_station, // r/o
      beamwidth@radar_station, // r/o
  FROM   timeslot_index, index, hdr, sat, radar_station
  WHERE	 obstype = $radar
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND kset = $kset
 ORDERBY seqno
;
