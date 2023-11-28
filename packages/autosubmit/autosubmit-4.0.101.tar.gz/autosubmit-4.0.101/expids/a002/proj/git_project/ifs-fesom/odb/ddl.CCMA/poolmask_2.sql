//
//-- ODB/SQL file 'poolmask_2.sql'
//
//   Last updated:  15-Oct-2001
//

SET $obstype  = -1;
SET $codetype = -1;
SET $sensor   = -1;
SET $tslot    = -1;

READONLY;

CREATE VIEW poolmask_2 AS
  SELECT DISTINCT poolno
    FROM poolmask
   WHERE (obstype  = $obstype  OR $obstype  = -1)
     AND (codetype = $codetype OR $codetype = -1)
     AND (sensor   = $sensor   OR $sensor   = -1)
     AND (timeslot    = $tslot    OR $tslot    = -1)
;
