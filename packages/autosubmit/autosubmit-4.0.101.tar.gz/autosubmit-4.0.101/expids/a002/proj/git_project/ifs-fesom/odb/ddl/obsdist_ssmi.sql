//
//-- ODB/SQL file 'obsdist_ssmi.sql'
//
//   Created:  22-Jun-2009
//

READONLY;

SET $pe = 0;
SET $obstype = -1;
SET $codetype = -1;
SET $sensor = -1;
SET $hdr_min = -1; 

// Make sure the SQL applies only to rows where sat.len@hdr & ssmi.len@sat are > 0 :
SAFEGUARD;

CREATE VIEW obsdist_ssmi AS
  SELECT distribid, seqno, window_offset, "*@ssmi"
    FROM hdr, sat, ssmi
    WHERE obstype = $satem
      AND codetype = $ssmi
      AND (obstype = $obstype OR $obstype = -1 )
      AND (codetype = $codetype OR $codetype = -1)
      AND (sensor = $sensor OR $sensor = -1)
      AND (window_offset = $hdr_min OR $hdr_min = -1)
      AND 1 <= distribid
      AND distribtype = 1
     AND paral($pe, distribid)
;
