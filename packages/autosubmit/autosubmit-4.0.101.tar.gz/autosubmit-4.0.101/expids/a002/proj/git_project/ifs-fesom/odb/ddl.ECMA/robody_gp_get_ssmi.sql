//
//-- ODB/SQL file 'robody_gp_get_ssmi.sql'
//

READONLY;

SET $tslot = -1;

CREATE VIEW robody_gp_get_ssmi AS

  SELECT seqno,         // MDBONM (used to build MLNKH2B)
         varno,         // MDBVNM (just is case we need this)
         vertco_type,   // MDBVCO (just is case we need this)
         datum_anflag,        // MDBFLG
         vertco_reference_1@body,    // MDBPPP
         obsvalue,      // MDBVAR

  FROM   timeslot_index, index, hdr, body

  WHERE  timeslot@timeslot_index == $tslot AND obstype == 7 AND codetype == 215 AND (sensor == 6 OR sensor == 9
OR sensor == 10 OR sensor == 17)
    AND  varno = $rawbt           // Brightness temp. i.e. 119
//  AND  vertco_type = $tovs_cha  // Note: commented out for now
;
