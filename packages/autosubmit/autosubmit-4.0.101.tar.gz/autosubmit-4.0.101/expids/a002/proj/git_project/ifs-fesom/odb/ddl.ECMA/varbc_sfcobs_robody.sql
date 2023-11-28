//
//-- ODB/SQL file 'varbc_sfcobs_robody.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_sfcobs_robody AS
  SELECT seqno,
         entryno,
         varno,
         ppcode@conv_body,
         obsvalue,
         varbc_ix@body UPDATED,
  FROM   timeslot_index, index, hdr, body, conv, conv_body
  WHERE  obstype in ($synop,$dribu,$paob) AND varno in ($ps,$apdss)
;

// Notes:
// 1. if the elements in the SELECT are changed, remember to update varbc_sfcobs.F90
// 2. if the list of varno in the WHERE are changed, remember to update
//        hdepart.F90, hretr.F90, hop.F90, hoptl.F90, and hopad.F90

