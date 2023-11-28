//
//-- ODB/SQL file 'robody.sql'
//
//   Last updated:  08/04/2010 A. Fouilloux Remove tcwv_fg
//                  2019-03-28 B. Ingleby   Add biascorr_fg
//
// Yannick: hardcoded 3 in obs_diags_*

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW robody_min AS   
  SELECT entryno, varno,               // r/o
         datum_anflag UPDATED,                           // possibly updated
         datum_event1@body UPDATED, datum_status@body UPDATED, // possibly updated
         an_depar UPDATED, fg_depar UPDATED,       // possibly updated
         actual_depar  UPDATED,                    // to pass actual departure from one subroutine to another (working ODB column)
         actual_ndbiascorr UPDATED,      // to pass normalised deviation from expected bias correction from one subroutine to another (work ODB column)
         hires@update[1:$NMXUPD] UPDATED,          // possibly updated
         lores@update[1:$NMXUPD] UPDATED,          // possibly updated
         qc_a UPDATED,                    // possibly updated
         qc_l UPDATED,                    // possibly updated
         qc_pge UPDATED,                    // possibly updated

         obs_diags_1@update[1:$NMXUPD] UPDATED,
         obs_diags_2@update[1:$NMXUPD] UPDATED,
         obs_diags_3@update[1:$NMXUPD] UPDATED,

         obsvalue,                     // r/o
         final_obs_error,              // r/o
         fg_error UPDATED,           // r/o
         fc_sens_obs UPDATED,      // r/o
         repres_error UPDATED,           // r/o
         obs_corr_ev[1:$NUMEV],          // r/o
         obs_corr_mask@errstat,          // r/o
         an_sens_obs UPDATED,            // r/o
         vertco_reference_1, vertco_reference_2,              // r/o
         varbc_ix,                     // r/o
         biascorr,                     // r/o
         biascorr_fg,                  // r/o  for switch_vwind
         jacobian_peak              UPDATED, // for OOPS framework
  FROM   timeslot_index, index, hdr, body, update[1:$NMXUPD], errstat
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
   ORDERBY seqno   
;
