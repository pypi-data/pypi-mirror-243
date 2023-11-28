//
//-- ODB/SQL file 'robhdr_mwave_update_smap.sql'
//

SET $hdr_min = 999;
SET $all     =-1;

CREATE VIEW robhdr_mwave_update_smap AS
  SELECT seqno,                       // r/o MUST BE FIRST hdr
         report_status,               // MDBRST hdr
         report_event1,               // MDBREV1 hdr
         gp_number,                   // MDB_GP_NUMBER hdr
         incidence_angle,             // MDB_TB_ANG_SMOS
         report_tbflag@smos,          // MDB_TB_FLAG_SMOS smos
         tbvalue@smos,                // MDB_TB_SMOS smos

  FROM   timeslot_index, index, hdr, smos
  WHERE  model_timestep@timeslot_index==$hdr_min AND reportype == 59001 AND obstype == 7 AND polarisation == $all 
