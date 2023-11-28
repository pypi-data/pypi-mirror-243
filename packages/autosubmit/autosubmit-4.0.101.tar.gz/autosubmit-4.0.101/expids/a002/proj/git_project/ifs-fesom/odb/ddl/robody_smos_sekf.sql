//
//-- ODB/SQL file 'robody_smos_sekf.sql'
//

READONLY;

SET $tslot = -1;
SET $kang_min = -1;
SET $kang_max = -1;

CREATE VIEW robody_smos_sekf AS

  SELECT seqno,           // MDBONM (used to build MLNKH2B)
         date,                          // MDBDAT hdr
         time,                          // MDBETM hdr
         lat,                           // MDBLAT hdr
         lon,                           // MDBLON hdr
         gp_number,                     // MDB_GP_NUMBER hdr
         incidence_angle,               // MDB_TB_ANG_SMOS smos
         polarisation@smos,             // MDB_POLARISATION_AT_SMOS smos
         rad_acc_pure@smos,             // MDB_RAD_ACC_PURE_SMOS smos
         report_tbflag@smos,            // MDB_TB_FLAG_SMOS smos
         varno,                         // MDBVNM body
         obsvalue,                      // MDBVAR body
         biascorr@body UPDATED,         // MDBTORB body
         model_timestep@timeslot_index,        // MDB_MODSTEP_AT_TIMESLOT_INDEX timeslot_index
  FROM   hdr, smos, body, timeslot_index
  WHERE reportype == 18001
    AND obstype == 7
    AND $kang_min <= incidence_angle <= $kang_max
    AND report_tbflag@smos == 1
