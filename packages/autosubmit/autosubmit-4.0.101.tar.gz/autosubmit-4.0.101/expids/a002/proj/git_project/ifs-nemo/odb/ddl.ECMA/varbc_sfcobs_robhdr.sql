//
//-- ODB/SQL file 'varbc_sfcobs_robhdr.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_sfcobs_robhdr AS
  SELECT seqno,
         body.len,
         statid, reportype, stalt
  FROM   index, hdr
  WHERE  obstype in ($synop,$dribu,$paob)
;

// Note:
//    if the elements in the SELE.CT are changed, remember to update varbc_sfcobs.F90

