//
//-- ODB/SQL file 'canaco_robhdr_ccma.sql'
//
//   Created : 21/02/2012
//

READONLY;

CREATE VIEW canaco_robhdr_ccma AS
  SELECT  seqno,
          body.len,
          obstype,
          sortbox,
          instrument_type,
          lon,
          lat,
          trlat
  FROM    index, hdr
  ORDERBY obstype, sortbox
;
