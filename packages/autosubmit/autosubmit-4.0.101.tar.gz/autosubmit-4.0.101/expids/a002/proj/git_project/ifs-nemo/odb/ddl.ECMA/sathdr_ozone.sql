//
//-- ODB/SQL file 'sathdr_ozone.sql'
//
//   Last updated:  02-Feb-2005
//

SET $tslot = -1;

CREATE VIEW sathdr_ozone AS
  SELECT seqno  READONLY,         // r/o; MUST BECOME FIRST
         satellite_identifier@sat,                   // r/o
         instrument_type@resat,    // r/o
         product_type,            // r/o
         scanpos@resat,            // r/o
         quality_retrieval,       // r/o
         number_layers,           // r/o
         lat_fovcorner[1:4],      // r/o
         lon_fovcorner[1:4],      // r/o
         solar_elevation,         // r/o
         cloud_cover,             // r/o
         cloud_top_press,         // r/o
         solar_zenith,            // r/o
         solar_azimuth,           // r/o
         zenith,        // r/o
         azimuth,       // r/o
         snow_ice_indicator,      // r/o
         retrsource,              // r/o
         surface_type_indicator,  // r/o
  FROM   timeslot_index, index, hdr, sat, resat
  WHERE	 obstype = $satem
    AND  codetype = $resat
    AND  (($tslot == -1 AND timeslot@timeslot_index > 0) OR (timeslot@timeslot_index == $tslot))
;
