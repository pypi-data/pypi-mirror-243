//
//-- ODB/SQL file 'varbc_gbrad_robhdr.sql'
//
//   For setting VarBC group indices

READONLY;

CREATE VIEW varbc_gbrad_robhdr AS
  SELECT seqno,
         subtype@hdr,
         source@hdr,
  FROM   index, hdr
  WHERE  codetype = $radrr AND obstype == $gbrad
;
