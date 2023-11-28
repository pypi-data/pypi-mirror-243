//
//-- ODB/SQL file 'obsortca_hdr2body.sql'
//
//   Last updated:  19-Jan-2000
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsortca_hdr2body AS
  SELECT target, seqno
  FROM index, hdr, body
  WHERE ($all >= 1 OR report_status.active@hdr = 1)
    AND ($all >= 1 OR datum_status.active@body = 1)
    AND (timeslot = 4) AND (obstype NOT IN ($satem,$scatt))
    AND ($all = 2 OR obstype IN ($synop,$dribu,$temp,$pilot,$paob)) 
    AND  paral($pe, target)
    ORDERBY seqno
;
