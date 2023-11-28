//
//-- ODB/SQL file 'conventional_robody_1.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;
SET $kobstype_v = 0; // Must be initialized to zero; used by in_vector()-function

CREATE VIEW conventional_robody_1 AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         entryno,                      // possibly updated
         vertco_type,                  // possibly updated
         varno,                        // possibly updated
         level@conv_body,              // possibly updated
         datum_event1,                 // possibly updated
         datum_event2,                 // possibly updated
         datum_status,                 // possibly updated
         datum_anflag,                 // possibly updated
         datum_rdbflag,                // possibly updated
         ppcode@conv_body,             // r/o
         obsvalue,                     // possibly updated
         vertco_reference_1,           // possibly updated
         vertco_reference_2,           // possibly updated
         datum_qcflag,                 // possibly updated 
         final_obs_error,              // possibly updated
         obs_error,                    // possibly updated
         pers_error,                   // possibly updated
         repres_error,                 // possibly updated
         fg_error,                     // possibly updated
         qc_a,                         // possibly updated
         qc_l,                         // possibly updated
         qc_pge,                       // possibly updated
         fg_depar,                     // possibly updated
         an_depar,                     // possibly updated
         biascorr,                     // possibly updated
  FROM   timeslot_index, index, hdr, body, errstat, conv, conv_body
//  WHERE  obstype IN ($synop, $airep, $dribu, $temp, $pilot, $paob)
  WHERE  in_vector(obstype, $kobstype_v)
    AND	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
