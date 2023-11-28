//
//-- ODB/SQL file 'obsort_hdr2scatt_body.sql'
//
//   Last updated:  13-Jan-2012
//

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW obsort_hdr2scatt_body AS
  SELECT target, seqno
    FROM index, hdr, sat, scatt, body, scatt_body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
     AND (#scatt_body >= 1)
     AND (scatt_body.len@scatt > 0)
     AND obstype = $scatt
     ORDERBY seqno
;
