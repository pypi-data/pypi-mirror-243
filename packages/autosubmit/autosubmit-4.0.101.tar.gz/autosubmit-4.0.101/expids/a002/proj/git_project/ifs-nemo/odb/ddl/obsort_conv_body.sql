//
//-- ODB/SQL file 'obsort_conv_body.sql'
//
//   Last updated:  22-Mar-2011
//

READONLY;

SET $all = 1;
SET $pe = 0;

CREATE VIEW obsort_conv_body AS
  SELECT target, seqno, "*@conv_body"
    FROM index, hdr, conv, conv_body, body
   WHERE conv_body.len > 0
     AND conv_body.len == body.len
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active@hdr = 1 AND datum_status.active@body = 1) )
     AND ( groupid = 17 OR obstype IN ($synop,$airep,$dribu,$temp,$pilot,$paob) ) //IFS OR AAA-H
     AND  paral($pe, target)
     ORDERBY seqno
;
