//
//-- ODB/SQL file 'date_time.sql'
//
//   Last updated:  18-May-2001
//

READONLY;

CREATE VIEW date_time AS
  SELECT date, time  // All r/o
    FROM hdr
;
