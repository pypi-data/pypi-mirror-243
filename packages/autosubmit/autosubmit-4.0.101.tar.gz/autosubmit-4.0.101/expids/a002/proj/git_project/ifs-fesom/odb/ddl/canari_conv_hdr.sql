//
//-- ODB/SQL file 'canari_conv.sql'
//
//   Last updated:  25-Mar-2011
//

READONLY;

SET $kset = 0;

CREATE VIEW canari_conv_hdr AS
  SELECT seqno,
         body.len,
         anemoht@conv,
//         baroht@conv
  FROM   index, hdr, conv
  WHERE  kset = $kset
  ORDERBY seqno
;
