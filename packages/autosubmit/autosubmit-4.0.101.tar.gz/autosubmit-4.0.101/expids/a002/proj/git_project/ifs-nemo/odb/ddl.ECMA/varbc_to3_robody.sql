//
//-- ODB/SQL file 'varbc_to3_robody.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_to3_robody AS
  SELECT seqno,   
	 nlayer@body,varno@body,
	 vertco_reference_1@body, vertco_reference_2@body,
         varbc_ix@body UPDATED,
  FROM   index, hdr, body
  WHERE  codetype = $resat
;
