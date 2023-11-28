//
//-- ODB/SQL file 'robody_raingg_get_rr.sql'
//

READONLY;

SET $hdr_min = 999;
SET $hdr_max = -1;
SET $tslot = -1;

CREATE VIEW robody_raingg_get_rr AS

  SELECT seqno,                 // MDBONM (used to build MLNKH2B)
         varno,                 // MDBVNM
         obsvalue,              // MDBVAR
         datum_status@body,     // MDBDSTA body
         rrvaluead@raingg_body, // MDB_RRVALUEAD  raingg_body

  FROM   timeslot_index, index, hdr, body, raingg_body

  WHERE  timeslot@timeslot_index == $tslot AND reportype == $hdr_max
    AND  varno == 203
;
