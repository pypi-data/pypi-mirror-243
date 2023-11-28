//
//-- ODB/SQL file 'obsdist_body.sql'
//
//   Created:  22-Jun-2009
//


READONLY;

SET $pe = 0;
SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;
SET $hdr_min = -1; // contains window offset

CREATE VIEW obsdist_body AS
  SELECT distribid, seqno, window_offset, "*@body"
    FROM hdr, body
     WHERE 1 <= distribid
       AND distribtype = 1
       AND (obstype = $obstype OR $obstype = -1 )
       AND (codetype = $codetype OR $codetype = -1)
       AND (sensor = $sensor OR $sensor = -1)
       AND (window_offset = $hdr_min OR $hdr_min = -1)
       AND paral($pe, distribid)
;
