//
//-- ODB/SQL file 'getactive_hdr2gbrad_body.sql'
//
//   Last updated:  22-July-2010
//

READONLY;

SET $all = 1;
SET $pe = 0;

NOREORDER; // Do not change the given table order in FROM-statement (important)

CREATE VIEW getactive_hdr2gbrad_body AS
  SELECT target, seqno
    FROM index, hdr, gbrad, body, gbrad_body
   WHERE (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1 AND distribtype IS NOT NULL) )
     AND (#gbrad_body >= 1)
     AND (gbrad_body.len@gbrad > 0)
     AND (obstype = $gbrad AND codetype = $radrr)
;
