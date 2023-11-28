//
//-- ODB/SQL file 'update_enkf_links.sql'
//
//   Last updated:  24/02/10
//   By          :  Anne Fouilloux

UPDATED;

CREATE VIEW update_enkf_links AS
  SELECT 
     body READONLY,         // r/o (offset + length)
     ensemble,                  // updated (offset + length)
    FROM hdr
;
