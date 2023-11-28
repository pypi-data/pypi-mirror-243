//
//-- ODB/SQL file 'satbody_allsky.sql'
//
//   New:  05-May-2010
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW satbody_allsky AS
  SELECT seqno  READONLY,              // r/o; MUST BECOME FIRST
       tbvalue@allsky_body,
       tbvaluead@allsky_body,
       tbvaluetl@allsky_body,
       datum_tbflag@allsky_body,
       emis_fg,
       emis_rtin,
       emis_retr,
       emis_atlas,
       tausfc,
       tbclear,               //  clear sky TB
       obs_error,             //     Only needed to pass an out-of-date qc check
       jacobian_peak,         // For Mats ENKF
       jacobian_hpeak,        // For Mats ENKF
       zenith_by_channel,
    FROM timeslot_index, index, hdr, allsky, body, allsky_body, errstat, radiance_body
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $allsky AND codetype = $ssmi
 ORDERBY seqno
;
