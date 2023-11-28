//
//-- ODB/SQL file 'varbc_gbrad_robody.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_gbrad_robody AS
  SELECT seqno,
         varbc_ix@body UPDATED,
  FROM   index, hdr, body
  WHERE  codetype = $radrr AND obstype == $gbrad AND varno == 203
;
