//
//-- ODB/SQL file 'robody_mwave_update_smos.sql'
//

SET $hdr_min = 999;
SET $all     = -1;

CREATE VIEW robody_mwave_update_smos AS

  SELECT seqno,                // r/o MUST BE FIRST hdr
         entryno,              //     
         varno,                //     MDBVNM   body
         obsvalue,             //     MDBVAR   body
         fg_depar,             //     MDBOMF   body
         datum_status@body,    //     MDBDSTA  body
         obs_error,            //     MDBOER   errstat

  FROM   timeslot_index, index, hdr, body, errstat, smos

  WHERE  model_timestep@timeslot_index==$hdr_min AND reportype == 18001 AND obstype == 7 AND varno == 190 AND polarisation == $all 
