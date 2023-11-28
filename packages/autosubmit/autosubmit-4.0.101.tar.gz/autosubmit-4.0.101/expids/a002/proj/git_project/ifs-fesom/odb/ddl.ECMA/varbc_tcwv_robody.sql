//
//-- ODB/SQL file 'varbc_tcwv_robody.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_tcwv_robody AS
  SELECT seqno,
         vertco_reference_1,
         varbc_ix@body UPDATED,
  FROM   index, hdr, body
  WHERE  codetype = $tcwc AND obstype == 7 AND varno == 9 AND sensor == 174
;
