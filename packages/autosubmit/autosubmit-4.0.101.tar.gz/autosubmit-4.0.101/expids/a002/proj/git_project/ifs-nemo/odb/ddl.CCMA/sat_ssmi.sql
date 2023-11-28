//
//-- ODB/SQL file 'sat_ssmi.sql'
//
//   Last updated:  13-Apr-2018
//

SET $tslot = -1;
SET $kset = 0;

CREATE VIEW sat_ssmi AS
  SELECT seqno  READONLY,         // r/o; MUST BECOME FIRST
         scanpos@radiance  READONLY,    // r/o
         gp_number,                   // MDB_GP_NUMBER hdr
         distribid,                   // MDB_DISTRIBID_AT_HDR hdr
         gp_dist,                     // MDB_GP_DIST
         satellite_identifier@sat,    // MDB_satid_AT_hdr
         zenith,                      // MDB_ZENITH_AT_SAT (in degrees)
         azimuth,                     // MDB_AZIMUTH_AT_SAT
         solar_zenith@sat  READONLY,  // r/o    probably junk
         lsm_fov,                     // MDB_LSM_FOV_AT_SAT
         fg_rain_rate,                // MDB_FG_RAIN_RATE
         fg_snow_rate,                // MDB_FG_SNOW_RATE
         fg_tcwv,                     // MDB_FG_TCWV
         fg_cwp,                      // MDB_FG_CWP
         fg_iwp,                      // MDB_FG_IWP
         fg_rwp,                      // MDB_FG_RWP
         fg_swp,                      // MDB_FG_SWP
         fg_rttov_cld_fraction,       // MDB_FG_RTTOV_CLD_FRAC
         fg_theta700,                 // MDB_FG_THETA700
         fg_thetasfc,                 // MDB_FG_THETASFC             
         fg_uth,                      // MDB_FG_UTH
         fg_conv,                     // MDB_FG_CONV
         fg_pbl,                      // MDB_FG_PBL
         an_rain_rate,                // MDB_AN_RAIN_RATE
         an_snow_rate,                // MDB_AN_SNOW_RATE
         an_tcwv,                     // MDB_AN_TCWV
         an_cwp,                      // MDB_AN_CWP
         an_iwp,                      // MDB_AN_IWP
         an_rwp,                      // MDB_AN_RWP
         an_swp,                      // MDB_AN_SWP
         an_rttov_cld_fraction,       // MDB_AN_RTTOV_CLD_FRAC
         an_theta700,                 // MDB_AN_THETA700
         an_thetasfc,                 // MDB_AN_THETASFC        
         an_uth,                      // MDB_AN_UTH
         an_conv,                     // MDB_AN_CONV
         an_pbl,                      // MDB_AN_PBL
         gnorm_10mwind,               // MDB_GNORM_10MWIND
         gnorm_skintemp,              // MDB_GNORM_SKINTEMP
         gnorm_temp,                  // MDB_GNORM_TEMP
         gnorm_q,                     // MDB_GNORM_Q
         gnorm_rainflux,              // MDB_GNORM_RAINFLUX
         gnorm_snowflux,              // MDB_GNORM_SNOWFLUX
         gnorm_clw,                   // MDB_GNORM_CLW
         gnorm_ciw,                   // MDB_GNORM_CIW 
         gnorm_cc,                    // MDB_GNORM_CC
         ob_p19, fg_p19, an_p19,      // MDB_OB_P19, MDB_FG_P19, MDB_AN_P19
         ob_p37, fg_p37, an_p37,      // MDB_OB_P37, MDB_FG_P37, MDB_AN_P37
         report_tbcloud,      
    FROM timeslot_index, index, hdr, sat, radiance, allsky
   WHERE (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
     AND kset = $kset
     AND obstype = $allsky 
     AND codetype = $ssmi
 ORDERBY seqno
;
