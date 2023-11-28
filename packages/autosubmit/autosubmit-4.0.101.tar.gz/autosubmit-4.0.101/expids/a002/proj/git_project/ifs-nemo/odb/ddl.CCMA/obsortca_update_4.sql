//
//-- ODB/SQL file 'obsortca_update_4.sql'
//
//   Last updated:  11-Apr-2003
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsortca_update_4 AS
  SELECT target, "/.*@update.*/"
  FROM index, hdr, update[min(4,$nmxupd)], body
  WHERE ($all >= 1 OR report_status.active@hdr = 1)
    AND ($all >= 1 OR datum_status.active@body = 1)
    AND (timeslot = 4) AND (obstype NOT IN ($satem,$scatt))
    AND ($all = 2 OR obstype IN ($synop,$dribu,$temp,$pilot,$paob)) 
    AND  paral($pe, target)
    ORDERBY seqno
;
