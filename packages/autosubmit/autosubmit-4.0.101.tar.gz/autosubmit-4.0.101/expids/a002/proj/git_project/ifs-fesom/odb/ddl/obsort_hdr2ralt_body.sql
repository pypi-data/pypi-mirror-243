//
//-- ODB/SQL file 'obsort_hdr2ralt_body.sql'
//
//   Last updated:  14-Aug-2014
//

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW obsort_hdr2ralt_body AS
  SELECT target, seqno
    FROM index, hdr, sat, body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND  paral($pe, target)
// we may need to replace the following two by something similar:
//     AND (#ralt_body >= 1)
//     AND (ralt_body.len@ralt > 0)
     AND obstype = $ralt 
;
