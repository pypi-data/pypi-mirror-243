//
//-- ODB/SQL file 'obsortca_index.sql'
//
//   Last updated:  19-Jan-2000
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsortca_index AS
  SELECT "*@index"
    FROM index, hdr
   WHERE ($all >= 1 OR report_status.active = 1)
     AND (timeslot = 4) AND (obstype NOT IN ($satem,$scatt))
     AND ($all = 2 OR obstype IN ($synop,$dribu,$temp,$pilot,$paob))
     AND  paral($pe, target)
     ORDERBY seqno
;
