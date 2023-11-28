//
//-- ODB/SQL file 'sufger_allsky.sql'
//
//   Last updated:  02-Feb-2005
//

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sufger_allsky AS
  SELECT seqno,                        // r/o; MUST BECOME FIRST
         body.len,                     // r/o
	 sensor,                       // r/o
         satellite_identifier@sat,     // r/o
         ob_p37, fg_p37, an_p37,       // r/o - used by all-sky mwave only
         zenith@sat,
  FROM   timeslot_index, index, hdr, sat, radiance, allsky
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
    AND  kset = $kset
;
