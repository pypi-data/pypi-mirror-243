//
//-- ODB/SQL file 'varbc_tcwv_robhdr.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_tcwv_robhdr AS
  SELECT seqno,
         satellite_identifier@sat,
         sensor,
  FROM   index, hdr, sat
  WHERE  codetype = $tcwc AND obstype == 7 AND sensor == 174
;
