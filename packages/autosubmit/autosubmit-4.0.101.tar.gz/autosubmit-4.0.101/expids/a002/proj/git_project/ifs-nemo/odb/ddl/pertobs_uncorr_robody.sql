//
//-- ODB/SQL file 'pertobs_uncorr_robody.sql'
//
//   Last updated:  02-Feb-2005
//

UPDATED; // the default: all updated (except those with  READONLY or  READONLY)

SET $kset = 0;
SET $tslot = -1;

CREATE VIEW pertobs_uncorr_robody AS
  SELECT seqno  READONLY,              // r/o; MUST BE FIRST
         datum_status@body READONLY,         // r/o
         vertco_reference_1@body READONLY,   // r/o
         final_obs_error READONLY,     // r/o
         obsvalue,                     // updated
         hires@update[1],              // updated
         fg_depar@body,                // updated
  FROM   timeslot_index, index, hdr, body, errstat, update[1]
  WHERE	 (kset = $kset)
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
;
