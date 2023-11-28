//
//-- ODB/SQL file 'obsdist_gbrad.sql'
//
//   Created:  22-July-2010
//

READONLY;
NOREORDER;

SET $pe = 0;
SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;
SET $hdr_min = -1; // contains window_offset

// Make sure the SQL applies only to rows where gbrad.len@hdr are > 0 :
SAFEGUARD;

CREATE VIEW obsdist_gbrad AS
  SELECT distribid, seqno, window_offset, "*@gbrad"
    FROM hdr, gbrad
    WHERE obstype = $gbrad
      AND codetype = $radrr
      AND (obstype = $obstype OR $obstype = -1 )
      AND (codetype = $codetype OR $codetype = -1)
      AND (sensor = $sensor OR $sensor = -1)
      AND (window_offset = $hdr_min OR $hdr_min = -1)
      AND 1 <= distribid
      AND distribtype = 1
      AND paral($pe, distribid)
;
