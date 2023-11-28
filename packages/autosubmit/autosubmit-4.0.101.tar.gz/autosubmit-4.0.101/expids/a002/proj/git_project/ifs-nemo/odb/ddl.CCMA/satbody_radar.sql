//
//-- ODB/SQL file 'satbody_radar.sql'
//
//   created : 15-Dec-2004
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW satbody_radar AS
  SELECT seqno  READONLY,                
         flgdyn,           // r/o; MUST BECOME FIRS
         distance,        // r/o 
         elevation,     // r/o 
         azimuth@radar_body,       // r/o 
         q[1]           UPDATED, //
         q[2]           UPDATED, //
         q_1dv          UPDATED,//
    FROM timeslot_index, index, hdr, sat, radar, radar_body
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $radar 
 ORDERBY seqno
;
