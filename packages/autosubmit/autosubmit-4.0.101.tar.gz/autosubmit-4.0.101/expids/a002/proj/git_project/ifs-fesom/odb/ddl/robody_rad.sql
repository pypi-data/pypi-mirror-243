//
//-- ODB/SQL file 'robody_rad.sql'
//
//   Last updated:  08/04/2010 A. Fouilloux Remove tcwv_fg
//
// Yannick: hardcoded 3 in obs_diags_*

READONLY;

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW robody_rad AS   
  SELECT seqno, 
         entryno, 
         varno,               // r/o
         datum_anflag,
         datum_event1@body UPDATED, 
         datum_status@body UPDATED, // possibly updated
         fg_depar UPDATED,       // possibly updated
         an_depar UPDATED,       // possibly updated
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
         obs_corr_ev[1:$NUMEV],          // r/o
         obs_corr_mask@errstat,          // r/o
         pers_error,                   // r/o
         vertco_reference_1, 
         varbc_ix,                     // r/o
         biascorr,
  FROM   timeslot_index, index, hdr, body, update[1:$NMXUPD], errstat
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
    AND obstype = $satem 
    AND codetype = $atovs
    AND (sensor!= $hirs OR (vertco_reference_1!=20))
    AND vertco_reference_1 IS NOT NULL 
    AND vertco_reference_1 > 0
    AND obsvalue IS NOT NULL
;
