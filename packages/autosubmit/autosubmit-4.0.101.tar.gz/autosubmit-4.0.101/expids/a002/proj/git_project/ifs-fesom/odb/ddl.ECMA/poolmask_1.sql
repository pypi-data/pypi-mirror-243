//
//-- ODB/SQL file 'poolmask_1.sql'
//
//   Last updated:  15-Oct-2001
//

SET $obstype  = -1;
SET $codetype = -1;
SET $sensor   = -1;

READONLY;

CREATE VIEW poolmask_1 AS
  SELECT DISTINCT poolno
    FROM poolmask
   WHERE (obstype  = $obstype  OR $obstype  = -1)
     AND (codetype = $codetype OR $codetype = -1)
     AND (sensor   = $sensor   OR $sensor   = -1)
;
