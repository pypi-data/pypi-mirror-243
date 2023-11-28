//
//-- ODB/SQL file 'flago_mobody.sql'
//
//   Last updated:  10-Oct-2001
//

UPDATED;

CREATE VIEW flago_mobody AS
SELECT
   seqno READONLY,
   entryno READONLY,
   datum_anflag,datum_status@body, datum_event1@body, datum_blacklist@body   
FROM hdr, body
