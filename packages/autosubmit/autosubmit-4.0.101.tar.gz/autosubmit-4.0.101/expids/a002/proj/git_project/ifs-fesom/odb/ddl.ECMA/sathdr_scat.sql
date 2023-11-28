//
//-- ODB/SQL file 'sathdr_scat.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;

CREATE VIEW sathdr_scat AS
  SELECT seqno  READONLY,         // r/o; MUST BECOME FIRST
         satellite_identifier@sat,                   // r/o
         cellno,                  // r/o
         prodflag,                // r/o
         wvc_qf,                  // r/o
         nretr_amb,               // r/o
  FROM   timeslot_index, index, hdr, sat, scatt
  WHERE	 obstype = $scatt
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
