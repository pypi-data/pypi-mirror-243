//
//-- ODB/SQL file 'suvarbc_robhdr_0.sql'
//
//   Last updated:  19-Mar-2004
//

READONLY;

CREATE VIEW suvarbc_robhdr_0 AS
  SELECT seqno  READONLY,              // r/o; MUST COME FIRST
         body.len  READONLY,           // r/o
         satellite_identifier@sat,                    // r/o
         sensor,                       // r/o
         codetype@hdr,                 // r/o
  FROM   index, hdr, sat
  WHERE  obstype = $satem
;
