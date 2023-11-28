//
//-- ODB/SQL file 'varbc_airep_robody.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_airep_robody AS
  SELECT seqno,
         vertco_reference_1,
         varbc_ix@body UPDATED,
  FROM   index, hdr, body
  WHERE  obstype == 2 AND varno == 2 and obsvalue IS NOT NULL
;
