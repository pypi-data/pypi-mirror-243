
//
//-- ODB/SQL file 'satbody_atovs.sql'
//
//


SET $tslot = -1;
SET $kset = 0;

CREATE VIEW satbody_atovs AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
         emis_rtin,
         emis_fg UPDATED,
         emis_retr,                    // possibly updated
         emis_atlas,                   // possibly updated
         emis_atlas_error,             // possibly updated
         tausfc UPDATED,
         channel_qc READONLY,          // r/o
         skintemp_retr,                // possibly updated
         cld_fg_depar,                 // possibly updated
         rank_cld,                     // possibly updated
         nobs_averaged READONLY,       // r/o
         stdev_averaged READONLY,      // r/o
         jacobian_peak,                // possibly updated
         jacobian_hpeak,               // possibly updated
         jacobian_peakl,               // possibly updated
         jacobian_hpeakl,              // possibly updated
         tbclear,                      // clear sky TB
         dust_aod_ir UPDATED,          // possibly updated
  FROM   timeslot_index, index, hdr, body, sat, radiance, radiance_body
  WHERE	 (($tslot == -1 AND timeslot@timeslot_index > 0) OR
(timeslot@timeslot_index == $tslot))
    AND  kset = $kset
    AND  obstype = $satem AND codetype = $atovs

 ORDERBY seqno
;
