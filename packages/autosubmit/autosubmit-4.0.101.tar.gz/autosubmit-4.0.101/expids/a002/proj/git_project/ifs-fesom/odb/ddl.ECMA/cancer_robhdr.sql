//
//-- ODB/SQL file 'cancer_robhdr.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW cancer_robhdr AS
  SELECT seqno,
         body.len,
         abnob, mapomm,
         obstype,
         codetype,
         lat,
         trlat,
         stalt,
         orography  UPDATED,
         lsm        UPDATED
  FROM   index, hdr, modsurf
;
