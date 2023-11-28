//
//-- ODB/SQL file 'data_radar_station.sql'
//
//   Last updated:  21-May-2008
//

READONLY;

CREATE VIEW data_radar_station AS
  SELECT DISTINCT *
  FROM radar_station
  ORDER BY ident
;
