//
//-- ODB/SQL file 'getactive_hdr2conv_body.sql'
//
//   Last updated:  22-Mar-2011
//

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW getactive_hdr2conv_body AS
  SELECT target, seqno
    FROM index, hdr, conv, body, conv_body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
     AND ( groupid = 17 OR obstype IN ($synop,$airep,$dribu,$temp,$pilot) ) //IFS OR AAA-H
     AND (#conv_body >= 1)
     AND (conv_body.len@conv > 0)
;
