//
//-- ODB/SQL file 'map_ssmi_rain_ssmi.sql'
//
//   Last updated:  18-May-2004
//

READONLY;

CREATE VIEW map_ssmi_rain_ssmi AS
  SELECT ssmi_body UPDATED // Update @LINK to ssmi_body (i.e. 2 columns)
  FROM   hdr, sat, ssmi
  WHERE	 bufrtype = 12
    AND  subtype  = 127
    AND  (sensor = 6 OR sensor = 10 OR sensor = 9 OR sensor = 17)
    AND  sat.len  = 1 // Play safe
    AND  ssmi.len = 1 // Play safe
;
