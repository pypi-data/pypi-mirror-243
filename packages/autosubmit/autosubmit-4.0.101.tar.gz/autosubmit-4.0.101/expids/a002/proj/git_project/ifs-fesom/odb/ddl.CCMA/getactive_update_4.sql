//
//-- ODB/SQL file 'getactive_update_4.sql'
//
//   Last updated:  20-Jul-2006
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_update_4 AS
  SELECT target, seqno, "/.*@update.*/"
    FROM index, hdr, update[min(4,$nmxupd)], body
   WHERE ( ($all = 1)
         OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
//   AND update_4.len > 0
//   AND update_4.len == body.len
;
