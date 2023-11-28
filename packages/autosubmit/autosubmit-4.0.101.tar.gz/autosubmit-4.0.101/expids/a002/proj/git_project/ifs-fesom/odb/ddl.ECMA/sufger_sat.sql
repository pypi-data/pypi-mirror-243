//
//-- ODB/SQL file 'sufger_sat.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sufger_sat AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         body.len,                     // r/o
         sensor,                       // r/o
         satellite_identifier@sat,     // r/o
         skintemper@radiance UPDATED,
  FROM   timeslot_index, index, hdr, sat, radiance
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND  kset = $kset
;
