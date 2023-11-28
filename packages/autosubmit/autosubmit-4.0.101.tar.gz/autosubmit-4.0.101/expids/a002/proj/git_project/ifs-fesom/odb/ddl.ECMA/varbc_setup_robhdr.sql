//
//-- ODB/SQL file 'varbc_setup_robhdr.sql'
//

READONLY;

CREATE VIEW varbc_setup_robhdr AS
  SELECT seqno,
         body.len,
         codetype@hdr,
  FROM   index, hdr
;
