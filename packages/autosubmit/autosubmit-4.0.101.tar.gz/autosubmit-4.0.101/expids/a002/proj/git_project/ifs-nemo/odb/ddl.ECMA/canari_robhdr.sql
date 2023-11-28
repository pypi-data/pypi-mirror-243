//
//-- ODB/SQL file 'canari_robhdr.sql'
//
//   08-May-2008 (F.Suzat added obstype)
//   19/12/2008 (D.Puech name changed)
//

READONLY;

SET $kset = 0;

CREATE VIEW canari_robhdr AS
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
  ORDERBY seqno
;
