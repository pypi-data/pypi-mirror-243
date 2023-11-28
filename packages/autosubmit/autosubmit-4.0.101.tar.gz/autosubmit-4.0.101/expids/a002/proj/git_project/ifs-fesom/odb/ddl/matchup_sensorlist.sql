//
//-- ODB/SQL file 'matchup_sensorlist.sql'
//
//   Last updated:  16-Aug-2006
//

READONLY;

SET $obstype = -1;
SET $codetype = -1;

CREATE VIEW matchup_sensorlist AS
  SELECT DISTINCT timeslot@index, sensor
    FROM index,hdr
   WHERE ($obstype  == -1 OR obstype  == $obstype)
     AND ($codetype == -1 OR codetype == $codetype)
     AND sensor is not NULL
 SORT BY timeslot@index, sensor
;
