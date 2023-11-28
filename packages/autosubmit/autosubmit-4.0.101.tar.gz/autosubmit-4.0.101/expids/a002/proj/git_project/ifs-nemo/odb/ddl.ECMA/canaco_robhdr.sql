//
//-- ODB/SQL file 'canaco_robhdr.sql'
//
//   Last updated:  10-Oct-2001 / 25-Jan-2012
//

READONLY;

CREATE VIEW canaco_robhdr AS
  SELECT  seqno,
          body.len,
          obstype,
          sortbox,
          instrument_type,
          report_blacklist,
          lon,
          lat,
          trlat,
          stalt,
          orography,
          lsm
  FROM    index, hdr, modsurf
  ORDERBY obstype, sortbox
;
