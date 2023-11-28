//
//-- ODB/SQL file 'hop_canari_conv.sql'
//
//   Last updated:  25-Mar-2011
//

READONLY;

SET $kset = 0;

CREATE VIEW hop_canari_conv AS
  SELECT seqno,
         body.len,
         anemoht@conv,
         baroht@conv
  FROM   index, hdr, conv
  WHERE  kset = $kset
;
