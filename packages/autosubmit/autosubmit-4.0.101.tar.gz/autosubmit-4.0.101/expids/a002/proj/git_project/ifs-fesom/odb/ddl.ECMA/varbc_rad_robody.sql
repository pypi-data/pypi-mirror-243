//
//-- ODB/SQL file 'varbc_rad_robody.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_rad_robody AS
  SELECT seqno,
         vertco_reference_1,
         varbc_ix@body UPDATED,
  FROM   index, hdr, body
  WHERE  codetype = $rad1c
;
