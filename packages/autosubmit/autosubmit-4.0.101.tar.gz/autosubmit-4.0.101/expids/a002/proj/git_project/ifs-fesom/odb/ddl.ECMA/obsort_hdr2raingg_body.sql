//
//-- ODB/SQL file 'obsort_hdr2raingg_body.sql'
//
//   Last updated:  22-July-2010
//

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW obsort_hdr2raingg_body AS
  SELECT target, seqno
    FROM index, hdr, raingg, body, raingg_body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1)
	  OR ($all = 2 ) )
     AND  paral($pe, target)
     AND (#raingg_body >= 1)
     AND (raingg_body.len@raingg > 0)
     AND (obstype = $raingg AND codetype = $radrr)
     ORDERBY seqno
;
