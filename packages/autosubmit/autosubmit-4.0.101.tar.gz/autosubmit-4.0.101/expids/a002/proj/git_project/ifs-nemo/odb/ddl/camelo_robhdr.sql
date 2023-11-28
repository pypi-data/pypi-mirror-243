//
//-- ODB/SQL file 'camelo_robhdr.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW camelo_robhdr AS
  SELECT seqno,
         body.len,
         codetype,
         instrument_type,
         obstype,
         sortbox UPDATED,
         trlat,
         date,
         lat,
         lon
  FROM   index, hdr
;
