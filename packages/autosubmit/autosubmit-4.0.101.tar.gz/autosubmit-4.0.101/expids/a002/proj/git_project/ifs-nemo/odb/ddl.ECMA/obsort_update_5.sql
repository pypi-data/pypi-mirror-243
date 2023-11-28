//
//-- ODB/SQL file 'obsort_update_5.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_update_5 AS
  SELECT target, seqno, "/.*@update.*/"
    FROM index, hdr, update[min(5,$nmxupd)], body
   WHERE ( ($all = 1)
         OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
//   AND update_5.len > 0
//   AND update_5.len == body.len
     AND  paral($pe, target)
     ORDERBY seqno
;
