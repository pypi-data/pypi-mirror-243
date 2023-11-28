//
//-- ODB/SQL file 'varbc_rsonde_robody.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_rsonde_robody AS
  SELECT seqno,
         reportype,
         statid,
         sonde_type,
         varbc_ix@body UPDATED,
         obsvalue,
  FROM   index, hdr, conv, body
  WHERE  obstype = $temp and varno = $t

;

// Notes:
// 1. if the elements in the SELE.CT are changed, remember to update varbc_rsonde.F90
// 2. if the list of varno in the WHE.RE are changed, remember to update
//        hdepart.F90, hop.F90, hoptl.F90, and hopad.F90

