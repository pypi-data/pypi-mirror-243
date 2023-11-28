//
//-- ODB/SQL file 'obsort_conv.sql'
//
//   Last updated:  22-Mar-2011
//

READONLY;

SET $all = 1;
SET $pe = 0;

// Make sure the SQL applies only to rows where conv.len@hdr are > 0 :
SAFEGUARD;

CREATE VIEW obsort_conv AS
  SELECT target, seqno, "*@conv"
    FROM index, hdr, conv
   WHERE conv.len > 0
     AND conv.len == hdr.len
     AND (   ($all = 1)
	  OR ($all = 0 AND report_status.active = 1) )
     AND ( groupid = 17 OR obstype IN ($synop,$airep,$dribu,$temp,$pilot,$paob) ) //IFS OR AAA-H
     AND  paral($pe, target)
     ORDERBY seqno
;
