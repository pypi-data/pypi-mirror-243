//
//-- ODB/SQL file 'xcheck.sql'
//
//   Last updated:  18-May-2001
//

READONLY;

CREATE VIEW xcheck AS
     SELECT andate, antime, hdr.len, source, version
       FROM desc
    SORT BY andate, antime
;
