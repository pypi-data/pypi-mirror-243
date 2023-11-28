//
//-- ODB/SQL file 'obsort_update.sql' (obsolete)
//
//   Last updated:  20-Jul-2006
//

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_update AS
  SELECT target, seqno, "*@update"
    FROM index, hdr, update, body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1)
	  OR ($all = 2 ) )
     AND  paral($pe, target)
     ORDERBY seqno
;
