//
//-- ODB/SQL file 'robody_smos_get_tb.sql'
//

READONLY;

SET $hdr_min = 999;
SET $all     = -1;

CREATE VIEW robody_mwave_process_smos AS

  SELECT seqno,           // MDBONM (used to build MLNKH2B)
         obsvalue,        // MDBVAR

  FROM   timeslot_index, index, hdr, body, smos
  WHERE  model_timestep@timeslot_index==$hdr_min AND reportype == 18001 AND obstype == 7 AND varno == 190 AND polarisation == $all
