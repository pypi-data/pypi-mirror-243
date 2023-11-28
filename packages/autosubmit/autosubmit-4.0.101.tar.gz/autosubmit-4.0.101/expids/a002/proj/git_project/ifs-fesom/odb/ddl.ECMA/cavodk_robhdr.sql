//
//-- ODB/SQL file 'cavodk_robhdr.sql'
//
//   Last updated:  10-Oct-2001
//

READONLY;

CREATE VIEW cavodk_robhdr AS
  SELECT  seqno,
          body.len,
          obstype,
          lon,
          lat,
          trlat,
          orography,
          lsm
  FROM    index, hdr, modsurf
;
