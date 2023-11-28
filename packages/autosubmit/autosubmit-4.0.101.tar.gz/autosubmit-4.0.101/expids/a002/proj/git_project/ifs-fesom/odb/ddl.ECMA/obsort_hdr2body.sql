//
//-- ODB/SQL file 'obsort_hdr2body.sql'
//
//   Last updated:  18-May-2001
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_hdr2body AS
  SELECT target, seqno
    FROM index, hdr, body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
     ORDERBY seqno
;
