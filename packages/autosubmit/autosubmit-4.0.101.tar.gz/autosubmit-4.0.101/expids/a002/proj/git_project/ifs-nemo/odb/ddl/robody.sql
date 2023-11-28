//
//-- ODB/SQL file 'robody.sql'
//
//   Last updated:  08/04/2010 A. Fouilloux Remove tcwv_fg
//   Last updated:  08/2018 F.Suzat report 43t2bf
//   Last updated:  26/09/2018 F. Duruisseau :  add variable for Bayrad
//
// Yannick: hardcoded 3 in obs_diags_*

UPDATED;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW robody AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         entryno READONLY,
         varno,
         datum_anflag UPDATED,                           // possibly updated
         datum_event1@body UPDATED, datum_status@body UPDATED, // possibly updated
         an_depar UPDATED, fg_depar UPDATED,       // possibly updated
         actual_depar  UPDATED,                    // to pass actual departure from one subroutine to another (working ODB column)
         actual_ndbiascorr UPDATED,      // to pass actual bias correction from one subroutine to another (work ODB column)
         hires@update[1:$NMXUPD] UPDATED,          // possibly updated
         lores@update[1:$NMXUPD] UPDATED,          // possibly updated
         qc_a UPDATED,                    // possibly updated
         qc_l UPDATED,                    // possibly updated
         qc_pge UPDATED,                    // possibly updated
         obs_diags_1@update[1:$NMXUPD] UPDATED,
         obs_diags_2@update[1:$NMXUPD] UPDATED,
         obs_diags_3@update[1:$NMXUPD] UPDATED,
         obsvalue,
         final_obs_error UPDATED,    // r/o
         fg_error UPDATED,           // r/o
         fc_sens_obs UPDATED,      // r/o
         repres_error UPDATED,           // r/o
         obs_corr_ev[1:$NUMEV],          // r/o
         obs_corr_mask@errstat,          // r/o
         an_sens_obs UPDATED,            // r/o
         mf_log_p UPDATED,
         mf_stddev UPDATED,
         mf_vertco_type UPDATED,
         vertco_reference_1,
         vertco_reference_2,
         varbc_ix READONLY,                     // r/o
         biascorr,
         datum_event2,
         datum_status,                 // possibly updated
         datum_blacklist,              // possibly updated
         datum_rdbflag,                // possibly updated
         vertco_type,                  // possibly updated
         obs_error,                    // possibly updated
         pers_error,                   // possibly updated
         biascorr_fg,                     // possibly updated
         jacobian_peak              UPDATED, // MDB_JACOBIAN_PEAK
         jacobian_hpeak             UPDATED, // MDB_JACOBIAN_HPEAK
         tbcorr@body,                  // possibly updated
         wdeff_bcorr@body,             // possibly updated
  FROM   timeslot_index, index, hdr, body, update[1:$NMXUPD], errstat
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
   ORDERBY seqno
;
