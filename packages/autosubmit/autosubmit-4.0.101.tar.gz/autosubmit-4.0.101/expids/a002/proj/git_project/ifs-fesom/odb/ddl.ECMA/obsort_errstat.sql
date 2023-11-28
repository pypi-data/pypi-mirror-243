//
//-- ODB/SQL file 'obsort_errstat.sql'
//
//   Last updated:  20-Jul-2006
//


READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_errstat AS
  SELECT target, seqno, "*@errstat"
    FROM index, hdr, errstat, body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
     ORDERBY seqno
;
