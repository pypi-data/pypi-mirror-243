//
//-- ODB/SQL file 'sat_radar.sql'
//

READONLY;

CREATE VIEW sat_radar AS
  SELECT satellite_identifier, 
         radar_station.offset UPDATED
  FROM sat
  WHERE radar_station.len>0
;
