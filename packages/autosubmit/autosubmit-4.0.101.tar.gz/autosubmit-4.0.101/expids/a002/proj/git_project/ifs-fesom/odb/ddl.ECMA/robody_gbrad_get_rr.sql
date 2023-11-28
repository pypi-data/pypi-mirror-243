//
//-- ODB/SQL file 'robody_gbrad_get_rr.sql'
//

READONLY;

SET $hdr_min = 999;
SET $hdr_max = 0;

CREATE VIEW robody_gbrad_get_rr AS

  SELECT seqno,                 // MDBONM (used to build MLNKH2B)
         varno,                 // MDBVNM
         obsvalue,              // MDBVAR
         datum_status@body,     // MDBDSTA body
         rrvaluead@gbrad_body,  // MDB_RRVALUEAD  gbrad_body
         retrtype@hdr,          // MDB_RETRTYPE_AT_HDR
         source@hdr,            // MDB_SOURCE_AT_HDR

  FROM   timeslot_index, index, hdr, body, gbrad_body

  WHERE  (timeslot@timeslot_index BETWEEN $hdr_min AND $hdr_max) 
    AND  codetype == 3 AND obstype == 14 AND varno == 203
;
