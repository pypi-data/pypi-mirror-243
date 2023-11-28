//
//-- ODB/SQL file 'caviso_robhdr.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW caviso_robhdr AS
  SELECT seqno,
         body.len,
         codetype,
         instrument_type,
         retrtype,
         obstype,
         sortbox,
         date,
         time,
         statid,
         trlat,
         lat,
         lon,
         stalt
  FROM   index, hdr
;
