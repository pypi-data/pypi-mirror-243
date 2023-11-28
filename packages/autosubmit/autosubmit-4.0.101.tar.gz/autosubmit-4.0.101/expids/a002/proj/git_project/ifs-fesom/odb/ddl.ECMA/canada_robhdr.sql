//
//-- ODB/SQL file 'canada_robhdr.sql'
//
//   08/01/2019 (D.Puech)
//

READONLY;

CREATE VIEW canada_robhdr AS
  SELECT seqno,
         body.len,
         obstype,sortbox,
         report_blacklist,
         lat, lon,
         instrument_type,
         lsm, orography,
  FROM   index, hdr, modsurf
  ORDERBY obstype,sortbox
;
