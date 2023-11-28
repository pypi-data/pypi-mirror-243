//
//-- ODB/SQL file 'caredo_robhdr_2.sql'
//
//   Last updated:  10-Oct-2001 / 25-Jan-2012
//

READONLY;

CREATE VIEW caredo_robhdr_2 AS
  SELECT  seqno,
          obstype,
          sortbox
  FROM    hdr
  ORDERBY obstype, sortbox
;
