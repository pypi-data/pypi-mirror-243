//
//-- ODB/SQL file 'links_ensemble.sql'
//
//   Last updated:  19-Jun-2012
//

UPDATED;

CREATE VIEW links_ensemble AS
  SELECT ensemble,
    body READONLY,
    FROM hdr
;
