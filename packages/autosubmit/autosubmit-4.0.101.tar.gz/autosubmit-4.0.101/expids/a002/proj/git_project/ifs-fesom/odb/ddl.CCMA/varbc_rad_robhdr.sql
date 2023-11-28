//
//-- ODB/SQL file 'varbc_rad_robhdr.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_rad_robhdr AS
  SELECT seqno,
         body.len,
         satellite_identifier@sat,
         sensor,
  FROM   index, hdr, sat
  WHERE  codetype = $rad1c
;
