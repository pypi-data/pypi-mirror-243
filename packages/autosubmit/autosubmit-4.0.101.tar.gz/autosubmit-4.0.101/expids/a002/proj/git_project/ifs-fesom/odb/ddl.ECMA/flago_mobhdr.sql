//
//-- ODB/SQL file 'flago_mobhdr.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW flago_mobhdr AS
SELECT
   seqno,
   abnob, mapomm,
   body.len,
   report_event1 UPDATED, report_blacklist UPDATED
FROM index, hdr
