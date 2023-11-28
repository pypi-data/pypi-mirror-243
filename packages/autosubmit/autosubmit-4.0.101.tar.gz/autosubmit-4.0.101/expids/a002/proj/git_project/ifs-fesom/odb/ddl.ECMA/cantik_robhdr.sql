//
//-- ODB/SQL file 'cantik_robhdr.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW cantik_robhdr AS
  SELECT seqno,
         body.len,
         obstype,
         trlat
  FROM   index, hdr
;
