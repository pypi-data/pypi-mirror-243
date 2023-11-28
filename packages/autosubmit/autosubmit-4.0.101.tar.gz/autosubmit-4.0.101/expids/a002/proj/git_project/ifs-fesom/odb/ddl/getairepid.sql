//
//-- ODB/SQL file 'getairepid.sql'
//
//   Last updated:  11-Jan-2016

//

READONLY;

CREATE VIEW getairepid AS
     SELECT DISTINCT statid@hdr, codetype
      FROM hdr, body
      WHERE obstype==$airep and codetype IN (141, 144, 145, 146, 148, 149) and
            varno==$t and obsvalue IS NOT NULL
      ORDERBY codetype, statid@hdr
;

