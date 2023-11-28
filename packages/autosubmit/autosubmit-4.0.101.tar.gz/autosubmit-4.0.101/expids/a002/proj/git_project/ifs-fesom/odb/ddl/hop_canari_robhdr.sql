//
//-- ODB/SQL file 'hop_canari_robhdr.sql'
//
//   Last updated:  08-May-2008 (F.Suzat added lon)
//

READONLY;

SET $kset = 0;

CREATE VIEW hop_canari_robhdr AS
  SELECT seqno,
         body.len,
         abnob, mapomm,
         obstype,
         codetype,
         lat,
         lon,
         stalt,
  FROM   index, hdr
  WHERE  kset = $kset
;
