//
//-- ODB/SQL file 'getgbradid.sql'
//
//   Last updated:  27-Sep-2010
//

READONLY;

CREATE VIEW getgbradid AS
     SELECT DISTINCT subtype@hdr, codetype, source@hdr
       FROM hdr
      WHERE obstype = $gbrad
      ORDERBY subtype@hdr, codetype
;
