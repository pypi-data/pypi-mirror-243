//
//-- ODB/SQL file 'robhdrca_obsort.sql'
//
//   Last updated:  19-Jan-2000
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW robhdrca_obsort AS
  SELECT lat, lon                //  r/o
  FROM index, hdr
  WHERE ($all >= 1 OR report_status.active = 1)
    AND (timeslot = 4)
    AND ($all = 2 OR $all = -2 OR obstype IN ($synop,$dribu,$temp,$pilot,$paob))
;
