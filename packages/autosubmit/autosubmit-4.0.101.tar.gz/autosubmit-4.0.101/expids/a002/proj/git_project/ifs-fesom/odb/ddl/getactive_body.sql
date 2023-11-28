//
//-- ODB/SQL file 'getactive_body.sql'
//
//   Last updated:  20-Jul-2006
//


READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW getactive_body AS
  SELECT target, seqno, "*@body"
    FROM index, hdr, body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
;
