//
//-- ODB/SQL file 'sathdr_satob.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;

CREATE VIEW sathdr_satob AS
  SELECT seqno  READONLY,         // r/o; MUST BECOME FIRST
         satellite_identifier@sat,                   // r/o
         comp_method,             // r/o
         instdata,                // r/o
         dataproc,                // r/o
         QI_fc,                 // r/o
         QI_nofc,               // r/o
         RFF,                    // r/o
         datastream,              // r/o
  FROM   timeslot_index, index, hdr, sat, satob
  WHERE	 obstype = $satob
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
