//
//-- ODB/SQL file 'sat_atovs_hyper.sql'
//
//   Last updated:  07-Jul-2018
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sat_atovs_hyper AS
  SELECT seqno  READONLY,                  // r/o; MUST BECOME FIRST
         cldcover READONLY,                // r/o; MUST BECOME FIRST
         skintemper,                       // possibly updated
         cldptop[1:3],                     // possibly updated
         cldne[1:3],                       // possibly updated
         skintemp[1:($NMXUPD+1)]@radiance, // possibly updated
         scatterindex_89_157 UPDATED,      // possibly updated
         scatterindex_23_89 UPDATED,       // possibly updated
         scatterindex_23_165 UPDATED,      // possibly updated
         lwp_obs UPDATED,                  // possibly updated
         t2m,
         typesurf UPDATED,
         surface_class,
         cldptop[1:3],                     // possibly updated
         cldne[1:3],                       // possibly updated
         scanpos@radiance  READONLY,       // r/o
         zenith@sat  READONLY,             // r/o
         azimuth@sat  READONLY,            // r/o
         solar_zenith@sat  READONLY,       // r/o
         solar_azimuth@sat  READONLY,      // r/o
         asr_pcloudy_high,                 // updated for overcast cloudy ir
         asr_pcloudy_middle  READONLY,     // r/o
         avhrr_stddev_ir    READONLY,    // r/o
         avhrr_stddev_ir2    READONLY,    // r/o
         avhrr_frac_cl1      READONLY,    // r/o
         avhrr_frac_cl2      READONLY,    // r/o
         avhrr_frac_cl3      READONLY,    // r/o
         avhrr_frac_cl4      READONLY,    // r/o
         avhrr_frac_cl5      READONLY,    // r/o
         avhrr_frac_cl6      READONLY,    // r/o
         avhrr_frac_cl7      READONLY,    // r/o
         avhrr_m_ir1_cl1     READONLY,    // r/o
         avhrr_m_ir1_cl2     READONLY,    // r/o
         avhrr_m_ir1_cl3     READONLY,    // r/o
         avhrr_m_ir1_cl4     READONLY,    // r/o
         avhrr_m_ir1_cl5     READONLY,    // r/o
         avhrr_m_ir1_cl6     READONLY,    // r/o
         avhrr_m_ir1_cl7     READONLY,    // r/o
         avhrr_m_ir2_cl1     READONLY,    // r/o
         avhrr_m_ir2_cl2     READONLY,    // r/o
         avhrr_m_ir2_cl3     READONLY,    // r/o
         avhrr_m_ir2_cl4     READONLY,    // r/o
         avhrr_m_ir2_cl5     READONLY,    // r/o
         avhrr_m_ir2_cl6     READONLY,    // r/o
         avhrr_m_ir2_cl7     READONLY,    // r/o
         avhrr_fg_ir1,                    // updated
         avhrr_fg_ir2,                    // updated
         avhrr_cloud_flag,                // updated
    FROM timeslot_index, index, hdr, sat, radiance, modsurf, collocated_imager_information
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $satem 
     AND codetype = $atovs
 ORDERBY seqno
;
