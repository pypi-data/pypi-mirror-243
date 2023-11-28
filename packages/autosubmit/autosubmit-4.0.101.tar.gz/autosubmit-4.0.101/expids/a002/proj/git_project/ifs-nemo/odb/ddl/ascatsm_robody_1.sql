//
//-- ODB/SQL file 'ascatsm_robody_1.sql'
//
//   Last updated:  06-Jun-2007
//

UPDATED;

SET $tslot = -1;
SET $codetype = -1;
SET $sensor = -1;

CREATE VIEW ascatsm_robody_1 AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         entryno,                      // possibly updated
         vertco_type,                  // possibly updated
         varno,                        // possibly updated
         reportype READONLY,           // r/o 
         datum_event1@body,                  // possibly updated
         datum_event2@body,                  // possibly updated
         datum_status@body,                  // possibly updated
         datum_anflag@body,                  // possibly updated
         datum_rdbflag@body,                 // possibly updated
         obsvalue,                     // possibly updated
         vertco_reference_1,           // possibly updated
         vertco_reference_2,           // possibly updated
         final_obs_error,              // possibly updated
         obs_error,                    // possibly updated
         pers_error,                   // possibly updated
         repres_error,                 // possibly updated
         fg_error,                     // possibly updated
         qc_a,                // possibly updated
         qc_l,                // possibly updated
         qc_pge,                // possibly updated
         fg_depar,                     // possibly updated
         an_depar,                     // possibly updated
  FROM   timeslot_index, index, hdr, body, errstat
  WHERE  obstype = $scatt
    AND  (($codetype == -1) OR (codetype == $codetype))
    AND  (($sensor == -1) OR (sensor == $sensor))
    AND         (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
