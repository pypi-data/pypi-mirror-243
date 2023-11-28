//
//-- ODB/SQL file 'varbc_allsky_robody.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_allsky_robody AS
  SELECT seqno,
         vertco_reference_1,          
         varbc_ix@body UPDATED,
  FROM   index, hdr, body
  WHERE  codetype = $ssmi AND obstype == $allsky AND varno == 119
;
