//
//-- ODB/SQL file 'castor.sql'
//
//   Last updated:  09-Oct-2001
//

READONLY;

CREATE VIEW castor AS
  SELECT kset UPDATED, abnob UPDATED, mapomm UPDATED,   // updated
     body.len,                       // r/o
     obstype,                        // r/o
     time, trlat,                    // r/o
    FROM index, hdr
;
