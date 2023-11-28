//
//-- ODB/SQL file 'radiance_averaging.sql'
//
//   Last updated:  01/02/2011
//


set $satellite_identifier=-1;
set $channel=-1;

READONLY;
CREATE VIEW radiance_averaging AS
  SELECT seqno, 
         entryno,
         orbit,
         time,
         scanpos UPDATED, 
         satellite_identifier,
         nobs_averaged UPDATED,
         stdev_averaged UPDATED,
         vertco_reference_1,
         obsvalue UPDATED,
         date, 
         scanline, 
         subtype,
         bufrtype,
         statid,
         lat UPDATED,
         lon UPDATED,
         stalt,
         numlev,
         sensor,
         satellite_instrument@sat,
         obstype,
         codetype,
         varno,
         vertco_type,
         gen_centre,
         gen_subcentre,
         zenith UPDATED,
         azimuth UPDATED,
         solar_zenith,
         solar_azimuth,
         reportype,
         groupid,
         channel_qc UPDATED,
    FROM hdr,sat, radiance, body, radiance_body
    where datastream=0
    and   satellite_identifier=$satellite_identifier
    and   vertco_reference_1=$channel
    orderby gen_centre, gen_subcentre, date, time, scanpos, orbit, scanline
;

