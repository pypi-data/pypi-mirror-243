//
//-- ODB/SQL file 'obsdist_smos.sql'
//
//   Created:  30-Jun-2010
//

READONLY;

SET $pe = 0;
SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;
SET $hdr_min = -1; // contains window_offset

// Make sure the SQL applies only to rows where sat.len@hdr & smos.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW obsdist_smos AS
  SELECT distribid, seqno, window_offset, "*@smos"
    FROM hdr, sat, smos
    WHERE obstype = $satem
      AND codetype = 400
      AND (obstype = $obstype OR $obstype = -1 )
      AND (codetype = $codetype OR $codetype = -1)
      AND (sensor = $sensor OR $sensor = -1)
      AND (window_offset = $hdr_min OR $hdr_min = -1)
      AND 1 <= distribid
      AND distribtype = 1
     AND paral($pe, distribid)
;
