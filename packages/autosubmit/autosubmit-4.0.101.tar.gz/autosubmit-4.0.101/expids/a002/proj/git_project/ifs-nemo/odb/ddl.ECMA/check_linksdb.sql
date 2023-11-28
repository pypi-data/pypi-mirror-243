//
//-- ODB/SQL file 'check_linksdb.sql'
//
//   Last updated:  20-Mar-2002
//

READONLY;

CREATE VIEW check_linksdb AS
  SELECT body, errstat, update[1:$nmxupd]
    FROM hdr
;
