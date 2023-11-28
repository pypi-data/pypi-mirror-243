//
//-- ODB/SQL file 'varbc_allsky_robhdr.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_allsky_robhdr AS
  SELECT seqno,
         satellite_identifier@sat,
         sensor,
  FROM   index, hdr, sat
  WHERE  codetype = $ssmi AND obstype == $allsky
;
