//
//-- ODB/SQL file 'robhdr_mwave_process_smap.sql'
//

READONLY; // .. except where  UPDATED qualifier was found

SET $hdr_min = 999;   // changed in the call to GETDB
SET $all     = -1;

CREATE VIEW robhdr_mwave_process_smap AS
  SELECT seqno,                         // MDBONM (must be the first index; used to build MLNKH2B)
         gp_number,                     // MDB_GP_NUMBER hdr
         gp_dist,                       // MDB_GP_DIST hdr
         incidence_angle,               // MDB_TB_ANG_SMOS
         report_tbflag@smos UPDATED,    // MDB_TB_FLAG_SMOS smos
  FROM   timeslot_index, index, hdr, smos
  WHERE  model_timestep@timeslot_index==$hdr_min AND reportype == 59001 AND obstype == 7 and polarisation == $all 

