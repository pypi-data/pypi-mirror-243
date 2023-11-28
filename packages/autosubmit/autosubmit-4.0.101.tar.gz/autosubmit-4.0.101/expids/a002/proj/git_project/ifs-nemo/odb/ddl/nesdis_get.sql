//
//-- ODB/SQL file 'nesdis_get.sql'
//
//   Last updated:  17-Dec-2012
//


READONLY;

CREATE VIEW nesdis_get AS // SSA-analysis (snow only); Get nesdis data
  SELECT seqno,                      // r/o; Must become first
         lat,
         lon,
         obsvalue,
         varno,                      // r/o
    FROM hdr, body
   WHERE obstype = $imsims
   AND varno =  $binary_snow_cover
   AND obsvalue IS NOT NULL
   ORDER BY lat DESC
;
